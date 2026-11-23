from __future__ import annotations

import csv
import io
import os
import re
import secrets
import sqlite3
from datetime import date, datetime, timedelta
from functools import wraps
from pathlib import Path

from flask import (
    Flask, abort, flash, g, jsonify, make_response, redirect, render_template,
    request, session, url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).resolve().parent


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32),
        DATABASE=os.environ.get("FILAZERO_DATABASE", str(Path(app.instance_path) / "filazero.sqlite3")),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "0") == "1",
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=15),
        DEMO_MODE=True,
    )
    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    def get_db() -> sqlite3.Connection:
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"], timeout=15, isolation_level=None)
            g.db.row_factory = sqlite3.Row
            g.db.execute("PRAGMA foreign_keys = ON")
            g.db.execute("PRAGMA busy_timeout = 15000")
        return g.db

    @app.teardown_appcontext
    def close_db(_error=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def now_iso() -> str:
        return datetime.now().isoformat(timespec="seconds")

    def migrate_appointments_unique(db: sqlite3.Connection) -> None:
        """DEF01: a restricao UNIQUE(user_id, slot_id) impedia reservar de novo apos cancelar.

        Bancos antigos sao reconstruidos sem a restricao, preservando o historico. A regra
        passa a ser: no maximo uma reserva ATIVA (booked/checked_in) por pessoa e horario.
        """
        table_sql = db.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='appointments'"
        ).fetchone()[0]
        if "UNIQUE(user_id, slot_id)" in table_sql:
            db.executescript(
                """
                PRAGMA foreign_keys = OFF;
                BEGIN;
                CREATE TABLE appointments_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    slot_id INTEGER NOT NULL REFERENCES slots(id),
                    status TEXT NOT NULL DEFAULT 'booked',
                    code TEXT NOT NULL UNIQUE,
                    created_at TEXT NOT NULL,
                    cancelled_at TEXT,
                    checked_in_at TEXT
                );
                INSERT INTO appointments_new SELECT id, user_id, slot_id, status, code, created_at,
                    cancelled_at, checked_in_at FROM appointments;
                DROP TABLE appointments;
                ALTER TABLE appointments_new RENAME TO appointments;
                CREATE INDEX IF NOT EXISTS idx_appointments_slot_status ON appointments(slot_id, status);
                COMMIT;
                PRAGMA foreign_keys = ON;
                """
            )
        db.execute(
            """CREATE UNIQUE INDEX IF NOT EXISTS uq_appointment_active_user_slot
               ON appointments(user_id, slot_id) WHERE status IN ('booked','checked_in')"""
        )

    def init_db() -> None:
        db = get_db()
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS units (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                neighborhood TEXT NOT NULL,
                address TEXT NOT NULL,
                opening_hours TEXT NOT NULL DEFAULT '07:00 às 19:00',
                is_open INTEGER NOT NULL DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                cpf TEXT UNIQUE,
                birth_date TEXT,
                phone TEXT,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('citizen','receptionist','manager')),
                unit_id INTEGER REFERENCES units(id),
                lgpd_consent INTEGER NOT NULL DEFAULT 0,
                consent_at TEXT,
                failed_attempts INTEGER NOT NULL DEFAULT 0,
                locked_until TEXT,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS queue_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id),
                unit_id INTEGER NOT NULL REFERENCES units(id),
                service TEXT NOT NULL,
                priority_declared INTEGER NOT NULL DEFAULT 0,
                priority_confirmed INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'waiting',
                created_at TEXT NOT NULL,
                present_at TEXT,
                called_at TEXT,
                started_at TEXT,
                completed_at TEXT,
                UNIQUE(user_id, id)
            );
            CREATE INDEX IF NOT EXISTS idx_queue_unit_status ON queue_entries(unit_id, status, created_at, id);
            CREATE UNIQUE INDEX IF NOT EXISTS uq_user_one_active_queue ON queue_entries(user_id)
              WHERE status IN ('waiting','present','called','attending');
            CREATE TABLE IF NOT EXISTS slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unit_id INTEGER NOT NULL REFERENCES units(id),
                service TEXT NOT NULL,
                slot_date TEXT NOT NULL,
                slot_time TEXT NOT NULL,
                capacity INTEGER NOT NULL CHECK(capacity > 0),
                active INTEGER NOT NULL DEFAULT 1,
                UNIQUE(unit_id, service, slot_date, slot_time)
            );
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id),
                slot_id INTEGER NOT NULL REFERENCES slots(id),
                status TEXT NOT NULL DEFAULT 'booked',
                code TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL,
                cancelled_at TEXT,
                checked_in_at TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_appointments_slot_status ON appointments(slot_id, status);
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id),
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL,
                read_at TEXT
            );
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES users(id),
                unit_id INTEGER REFERENCES units(id),
                action TEXT NOT NULL,
                details TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        migrate_appointments_unique(db)

        if db.execute("SELECT COUNT(*) FROM units").fetchone()[0] == 0:
            demo_units = [
                ("UBS Demonstrativa - Centro", "Centro", "Endereço demonstrativo, Salvador - BA", "07:00 às 19:00", 1),
                ("UBS Demonstrativa - Brotas", "Brotas", "Endereço demonstrativo, Salvador - BA", "07:00 às 19:00", 1),
                ("UBS Demonstrativa - Itapuã", "Itapuã", "Endereço demonstrativo, Salvador - BA", "07:00 às 19:00", 1),
            ]
            db.executemany(
                "INSERT INTO units(name, neighborhood, address, opening_hours, is_open) VALUES(?,?,?,?,?)",
                demo_units,
            )

        # Contas de demonstração para apresentar os perfis. Troque as senhas antes de qualquer publicação.
        demo_accounts = [
            ("Recepção Demonstração", None, None, "71990000001", "recepcao@filazero.local", "Recepcao@123", "receptionist", 1),
            ("Gestor Demonstração", None, None, "71990000002", "gestor@filazero.local", "Gestor@123", "manager", 1),
        ]
        if app.config["DEMO_MODE"]:
            demo_accounts.append(
                ("Cidadão Demonstração", None, None, None, "cidadao@filazero.local", "Cidadao@123", "citizen", None),
            )
        for name, cpf, birth, phone, email, password, role, unit_id in demo_accounts:
            if not db.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone():
                db.execute(
                    """INSERT INTO users(name, cpf, birth_date, phone, email, password_hash, role, unit_id,
                       created_at) VALUES(?,?,?,?,?,?,?,?,?) ON CONFLICT(email) DO NOTHING""",
                    (name, cpf, birth, phone, email, generate_password_hash(password), role, unit_id, now_iso()),
                )

        # Horários fictícios para demonstração; não representam agenda de uma UBS real.
        today = date.today()
        for unit in db.execute("SELECT id FROM units").fetchall():
            for day_offset in range(1, 8):
                target = (today + timedelta(days=day_offset)).isoformat()
                for service, times, capacity in [
                    ("Consulta clínica", ["08:00", "09:00", "10:00", "14:00"], 4),
                    ("Vacinação", ["08:30", "09:30", "15:00"], 6),
                    ("Exames", ["07:30", "11:00", "13:30"], 3),
                ]:
                    for slot_time in times:
                        db.execute(
                            """INSERT OR IGNORE INTO slots(unit_id, service, slot_date, slot_time, capacity)
                               VALUES(?,?,?,?,?)""",
                            (unit["id"], service, target, slot_time, capacity),
                        )

    @app.before_request
    def initialize_and_protect():
        if not getattr(app, "_db_initialized", False):
            init_db()
            app._db_initialized = True

        if request.endpoint == "static":
            return None
        if session.get("user_id"):
            last_seen = session.get("last_seen")
            if last_seen and datetime.now() - datetime.fromtimestamp(last_seen) > timedelta(minutes=15):
                session.clear()
                flash("Sua sessão expirou por inatividade. Entre novamente.", "warning")
            else:
                session["last_seen"] = datetime.now().timestamp()
                session.permanent = True

        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            expected = session.get("csrf_token", "")
            supplied = request.form.get("csrf_token") or request.headers.get("X-CSRF-Token", "")
            if not expected or not secrets.compare_digest(expected, supplied):
                abort(400, description="Token de segurança inválido. Atualize a página e tente novamente.")
        return None

    @app.context_processor
    def inject_globals():
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_urlsafe(32)
        user = None
        if session.get("user_id"):
            user = get_db().execute(
                "SELECT id, name, email, role, unit_id FROM users WHERE id=?", (session["user_id"],)
            ).fetchone()
        unread = 0
        if user and user["role"] == "citizen":
            unread = get_db().execute(
                "SELECT COUNT(*) FROM notifications WHERE user_id=? AND read_at IS NULL", (user["id"],)
            ).fetchone()[0]
        return {"current_user": user, "csrf_token": session["csrf_token"], "unread_notifications": unread}

    def login_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get("user_id"):
                flash("Entre na sua conta para continuar.", "info")
                return redirect(url_for("login", next=request.path))
            return view(*args, **kwargs)
        return wrapped

    def roles_required(*roles):
        def decorator(view):
            @wraps(view)
            @login_required
            def wrapped(*args, **kwargs):
                user = get_db().execute("SELECT role FROM users WHERE id=?", (session["user_id"],)).fetchone()
                if not user or user["role"] not in roles:
                    abort(403)
                return view(*args, **kwargs)
            return wrapped
        return decorator

    def current_user():
        return get_db().execute("SELECT * FROM users WHERE id=?", (session.get("user_id"),)).fetchone()

    def audit(action: str, details: str, unit_id: int | None = None):
        get_db().execute(
            "INSERT INTO audit_logs(user_id, unit_id, action, details, created_at) VALUES(?,?,?,?,?)",
            (session.get("user_id"), unit_id, action, details[:500], now_iso()),
        )

    def notify(user_id: int, title: str, message: str):
        get_db().execute(
            "INSERT INTO notifications(user_id, title, message, created_at) VALUES(?,?,?,?)",
            (user_id, title, message, now_iso()),
        )

    def digits(value: str) -> str:
        return re.sub(r"\D", "", value or "")

    def valid_cpf(value: str) -> bool:
        cpf = digits(value)
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        for length in (9, 10):
            total = sum(int(cpf[i]) * (length + 1 - i) for i in range(length))
            digit = (total * 10) % 11
            if digit == 10:
                digit = 0
            if digit != int(cpf[length]):
                return False
        return True

    def masked_cpf(value: str | None) -> str:
        cpf = digits(value or "")
        return f"***.***.{cpf[6:9]}-**" if len(cpf) == 11 else "Não informado"

    def active_queue_for_user(user_id: int):
        return get_db().execute(
            """SELECT q.*, u.name AS unit_name, u.neighborhood
               FROM queue_entries q JOIN units u ON u.id=q.unit_id
               WHERE q.user_id=? AND q.status IN ('waiting','present','called','attending')
               ORDER BY q.created_at DESC LIMIT 1""",
            (user_id,),
        ).fetchone()

    def queue_snapshot(entry_id: int):
        db = get_db()
        entry = db.execute("SELECT * FROM queue_entries WHERE id=?", (entry_id,)).fetchone()
        if not entry:
            return None
        if entry["status"] not in ("waiting", "present"):
            return {"position": None, "ahead": 0, "estimated_minutes": 0}
        before = db.execute(
            """SELECT COUNT(*) FROM queue_entries
               WHERE unit_id=? AND status IN ('waiting','present')
                 AND (priority_confirmed > ? OR (priority_confirmed = ? AND
                      (created_at < ? OR (created_at = ? AND id < ?))))""",
            (entry["unit_id"], entry["priority_confirmed"], entry["priority_confirmed"],
             entry["created_at"], entry["created_at"], entry["id"]),
        ).fetchone()[0]
        return {"position": before + 1, "ahead": before, "estimated_minutes": (before + 1) * 15}

    def expire_calls(unit_id: int):
        db = get_db()
        cutoff = (datetime.now() - timedelta(minutes=5)).isoformat(timespec="seconds")
        expired = db.execute(
            "SELECT id, user_id FROM queue_entries WHERE unit_id=? AND status='called' AND called_at < ?",
            (unit_id, cutoff),
        ).fetchall()
        for item in expired:
            db.execute("UPDATE queue_entries SET status='no_show' WHERE id=?", (item["id"],))
            notify(item["user_id"], "Chamada expirada", "O prazo de 5 minutos para comparecimento terminou. Procure a recepção.")
            audit("marcar_ausente", f"Fila #{item['id']} marcada como ausente por expiração.", unit_id)

    @app.get("/")
    def index():
        units = get_db().execute("SELECT * FROM units ORDER BY neighborhood").fetchall()
        return render_template("index.html", units=units)

    @app.route("/cadastro", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            cpf = digits(request.form.get("cpf", ""))
            birth_date = request.form.get("birth_date", "").strip()
            phone = digits(request.form.get("phone", ""))
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            consent = request.form.get("lgpd_consent") == "on"
            errors = []
            if len(name) < 3:
                errors.append("Informe seu nome completo.")
            if not valid_cpf(cpf):
                errors.append("CPF inválido. Confira os números digitados.")
            try:
                date.fromisoformat(birth_date)
            except ValueError:
                errors.append("Informe uma data de nascimento válida.")
            if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                errors.append("Informe um e-mail válido.")
            if len(password) < 8:
                errors.append("A senha deve possuir pelo menos 8 caracteres.")
            if not consent:
                errors.append("É necessário aceitar o termo de consentimento para concluir o cadastro.")
            db = get_db()
            if db.execute("SELECT id FROM users WHERE cpf=? OR email=?", (cpf, email)).fetchone():
                errors.append("Já existe cadastro com este CPF ou e-mail.")
            if errors:
                for error in errors:
                    flash(error, "error")
                return render_template("register.html")
            db.execute(
                """INSERT INTO users(name, cpf, birth_date, phone, email, password_hash, role,
                   lgpd_consent, consent_at, created_at) VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (name, cpf, birth_date, phone, email, generate_password_hash(password), "citizen", 1, now_iso(), now_iso()),
            )
            flash("Cadastro concluído! Agora entre com seu CPF ou e-mail.", "success")
            return redirect(url_for("login"))
        return render_template("register.html")

    @app.route("/entrar", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            identifier = request.form.get("identifier", "").strip()
            password = request.form.get("password", "")
            db = get_db()
            user = db.execute(
                "SELECT * FROM users WHERE email=? COLLATE NOCASE OR cpf=?",
                (identifier.lower(), digits(identifier)),
            ).fetchone()
            generic_error = "Não foi possível entrar. Confira suas credenciais ou tente novamente mais tarde."
            if user:
                if user["locked_until"] and datetime.fromisoformat(user["locked_until"]) > datetime.now():
                    flash("Acesso temporariamente bloqueado após 5 tentativas. Tente novamente em 15 minutos.", "error")
                    return render_template("login.html")
                if not check_password_hash(user["password_hash"], password):
                    attempts = user["failed_attempts"] + 1
                    locked_until = (datetime.now() + timedelta(minutes=15)).isoformat(timespec="seconds") if attempts >= 5 else None
                    db.execute(
                        "UPDATE users SET failed_attempts=?, locked_until=? WHERE id=?",
                        (0 if locked_until else attempts, locked_until, user["id"]),
                    )
                    flash(generic_error, "error")
                    return render_template("login.html")
                db.execute("UPDATE users SET failed_attempts=0, locked_until=NULL WHERE id=?", (user["id"],))
                session.clear()
                session["user_id"] = user["id"]
                session["last_seen"] = datetime.now().timestamp()
                session.permanent = True
                session["csrf_token"] = secrets.token_urlsafe(32)
                audit("login", f"Login realizado como {user['role']}.", user["unit_id"])
                if user["role"] == "citizen":
                    return redirect(url_for("dashboard"))
                return redirect(url_for("staff_dashboard"))
            flash(generic_error, "error")
        return render_template("login.html")

    @app.post("/sair")
    @login_required
    def logout():
        session.clear()
        flash("Você saiu do FilaZero com segurança.", "success")
        return redirect(url_for("index"))

    @app.get("/painel")
    @roles_required("citizen")
    def dashboard():
        user = current_user()
        active_entry = active_queue_for_user(user["id"])
        position = queue_snapshot(active_entry["id"]) if active_entry else None
        appointments = get_db().execute(
            """SELECT a.*, s.service, s.slot_date, s.slot_time, u.name AS unit_name
               FROM appointments a JOIN slots s ON s.id=a.slot_id JOIN units u ON u.id=s.unit_id
               WHERE a.user_id=? AND a.status='booked' ORDER BY s.slot_date, s.slot_time LIMIT 3""",
            (user["id"],),
        ).fetchall()
        return render_template("dashboard.html", active_entry=active_entry, position=position, appointments=appointments)

    @app.get("/unidades")
    @roles_required("citizen")
    def units():
        term = request.args.get("q", "").strip()
        sql = "SELECT * FROM units"
        params: tuple = ()
        if term:
            sql += " WHERE neighborhood LIKE ? OR name LIKE ? OR address LIKE ?"
            params = (f"%{term}%", f"%{term}%", f"%{term}%")
        sql += " ORDER BY neighborhood"
        results = get_db().execute(sql, params).fetchall()
        return render_template("units.html", units=results, term=term)

    @app.post("/fila/entrar")
    @roles_required("citizen")
    def join_queue():
        db = get_db()
        user = current_user()
        unit_id = request.form.get("unit_id", type=int)
        service = request.form.get("service", "").strip()
        declared = request.form.get("priority_declared") == "on"
        unit = db.execute("SELECT * FROM units WHERE id=?", (unit_id,)).fetchone()
        if not unit or not service:
            flash("Selecione uma unidade e um serviço válido.", "error")
            return redirect(url_for("units"))
        if not unit["is_open"]:
            flash("A fila desta unidade está encerrada no momento. Consulte os agendamentos.", "warning")
            return redirect(url_for("units"))
        if active_queue_for_user(user["id"]):
            flash("Você já possui uma fila ativa. Cancele ou conclua a atual antes de entrar em outra.", "warning")
            return redirect(url_for("dashboard"))
        try:
            db.execute(
                """INSERT INTO queue_entries(user_id, unit_id, service, priority_declared,
                   priority_confirmed, status, created_at) VALUES(?,?,?,?,?,?,?)""",
                (user["id"], unit_id, service, 1 if declared else 0, 0, "waiting", now_iso()),
            )
        except sqlite3.IntegrityError:
            flash("Você já possui uma fila ativa. Atualize o painel para consultar sua posição.", "warning")
            return redirect(url_for("dashboard"))
        entry_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        snapshot = queue_snapshot(entry_id)
        notify(user["id"], "Entrada confirmada", f"Você entrou na fila de {unit['name']}. Sua posição inicial é {snapshot['position']}.")
        flash("Você entrou na fila virtual! A prioridade declarada será confirmada pela recepção.", "success")
        return redirect(url_for("my_queue"))

    @app.get("/minha-fila")
    @roles_required("citizen")
    def my_queue():
        entry = active_queue_for_user(current_user()["id"])
        position = queue_snapshot(entry["id"]) if entry else None
        return render_template("my_queue.html", entry=entry, position=position)

    @app.post("/fila/cancelar/<int:entry_id>")
    @roles_required("citizen")
    def cancel_queue(entry_id: int):
        db = get_db()
        entry = db.execute("SELECT * FROM queue_entries WHERE id=? AND user_id=?", (entry_id, session["user_id"])).fetchone()
        if not entry or entry["status"] not in ("waiting", "present", "called"):
            flash("Esta fila não pode mais ser cancelada.", "error")
        else:
            db.execute("UPDATE queue_entries SET status='cancelled' WHERE id=?", (entry_id,))
            audit("cancelar_fila", f"Fila #{entry_id} cancelada pelo cidadão.", entry["unit_id"])
            flash("Saída da fila registrada.", "success")
        return redirect(url_for("dashboard"))

    @app.get("/agendamentos")
    @roles_required("citizen")
    def appointments():
        user = current_user()
        db = get_db()
        slots = db.execute(
            """SELECT s.*, u.name AS unit_name, u.neighborhood,
                      (SELECT COUNT(*) FROM appointments a WHERE a.slot_id=s.id AND a.status IN ('booked','checked_in')) AS booked
               FROM slots s JOIN units u ON u.id=s.unit_id
               WHERE s.active=1 AND s.slot_date>=? ORDER BY s.slot_date, s.slot_time LIMIT 150""",
            (date.today().isoformat(),),
        ).fetchall()
        mine = db.execute(
            """SELECT a.*, s.service, s.slot_date, s.slot_time, u.name AS unit_name
               FROM appointments a JOIN slots s ON s.id=a.slot_id JOIN units u ON u.id=s.unit_id
               WHERE a.user_id=? ORDER BY s.slot_date DESC, s.slot_time DESC LIMIT 30""",
            (user["id"],),
        ).fetchall()
        return render_template("appointments.html", slots=slots, mine=mine)

    @app.post("/agendamentos/criar")
    @roles_required("citizen")
    def book_slot():
        db = get_db()
        slot_id = request.form.get("slot_id", type=int)
        # BEGIN IMMEDIATE serializa as reservas concorrentes na mesma base SQLite.
        db.execute("BEGIN IMMEDIATE")
        try:
            slot = db.execute("SELECT * FROM slots WHERE id=? AND active=1", (slot_id,)).fetchone()
            if not slot or slot["slot_date"] < date.today().isoformat():
                db.rollback()
                flash("Este horário não está mais disponível.", "error")
                return redirect(url_for("appointments"))
            existing = db.execute(
                "SELECT id FROM appointments WHERE user_id=? AND slot_id=? AND status IN ('booked','checked_in')",
                (session["user_id"], slot_id),
            ).fetchone()
            booked = db.execute(
                "SELECT COUNT(*) FROM appointments WHERE slot_id=? AND status IN ('booked','checked_in')", (slot_id,)
            ).fetchone()[0]
            if existing or booked >= slot["capacity"]:
                db.rollback()
                flash("A vaga foi ocupada ou você já possui reserva neste horário. Escolha outro horário.", "warning")
                return redirect(url_for("appointments"))
            code = "FZ-" + secrets.token_hex(3).upper()
            db.execute(
                "INSERT INTO appointments(user_id, slot_id, status, code, created_at) VALUES(?,?,?,?,?)",
                (session["user_id"], slot_id, "booked", code, now_iso()),
            )
            db.commit()
            notify(session["user_id"], "Agendamento confirmado", f"Seu código de confirmação é {code}.")
            flash(f"Agendamento confirmado! Código: {code}.", "success")
        except Exception:
            db.rollback()
            raise
        return redirect(url_for("appointments"))

    @app.post("/agendamentos/cancelar/<int:appointment_id>")
    @roles_required("citizen")
    def cancel_appointment(appointment_id: int):
        db = get_db()
        appointment = db.execute(
            "SELECT * FROM appointments WHERE id=? AND user_id=?", (appointment_id, session["user_id"])
        ).fetchone()
        if not appointment or appointment["status"] != "booked":
            flash("Este agendamento não pode ser cancelado.", "error")
        else:
            db.execute(
                "UPDATE appointments SET status='cancelled', cancelled_at=? WHERE id=?",
                (now_iso(), appointment_id),
            )
            notify(session["user_id"], "Agendamento cancelado", "Sua vaga foi liberada para outro cidadão.")
            flash("Agendamento cancelado e vaga liberada.", "success")
        return redirect(url_for("appointments"))

    @app.get("/notificacoes")
    @roles_required("citizen")
    def notifications():
        db = get_db()
        db.execute("UPDATE notifications SET read_at=? WHERE user_id=? AND read_at IS NULL", (now_iso(), session["user_id"]))
        items = db.execute(
            "SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC LIMIT 50", (session["user_id"],)
        ).fetchall()
        return render_template("notifications.html", items=items)

    @app.get("/equipe")
    @roles_required("receptionist", "manager")
    def staff_dashboard():
        user = current_user()
        unit_id = user["unit_id"]
        if not unit_id:
            abort(403)
        expire_calls(unit_id)
        queue = get_db().execute(
            """SELECT q.*, u.name AS citizen_name, u.cpf AS citizen_cpf, u.phone
               FROM queue_entries q JOIN users u ON u.id=q.user_id
               WHERE q.unit_id=? AND q.status IN ('waiting','present','called','attending')
               ORDER BY CASE WHEN q.status IN ('called','attending') THEN 0 ELSE 1 END,
                        q.priority_confirmed DESC, q.created_at, q.id""",
            (unit_id,),
        ).fetchall()
        search = request.args.get("q", "").strip()
        found = []
        found_appointments = []
        if search:
            found = get_db().execute(
                """SELECT q.*, u.name AS citizen_name, u.cpf AS citizen_cpf
                   FROM queue_entries q JOIN users u ON u.id=q.user_id
                   WHERE q.unit_id=? AND q.status IN ('waiting','present')
                     AND (u.name LIKE ? OR u.cpf LIKE ?) ORDER BY q.created_at LIMIT 10""",
                (unit_id, f"%{search}%", f"%{digits(search)}%"),
            ).fetchall()
            found_appointments = get_db().execute(
                """SELECT a.id AS appointment_id, a.user_id, a.status AS appointment_status,
                          s.service, s.slot_date, s.slot_time, u.name AS citizen_name, u.cpf AS citizen_cpf
                   FROM appointments a JOIN slots s ON s.id=a.slot_id JOIN users u ON u.id=a.user_id
                   WHERE s.unit_id=? AND s.slot_date=? AND a.status='booked'
                     AND (u.name LIKE ? OR u.cpf LIKE ?) ORDER BY s.slot_time LIMIT 10""",
                (unit_id, date.today().isoformat(), f"%{search}%", f"%{digits(search)}%"),
            ).fetchall()
        unit = get_db().execute("SELECT * FROM units WHERE id=?", (unit_id,)).fetchone()
        return render_template("staff.html", queue=queue, found=found, found_appointments=found_appointments,
                               search=search, unit=unit)

    @app.post("/equipe/presenca")
    @roles_required("receptionist", "manager")
    def confirm_presence():
        user = current_user()
        entry_id = request.form.get("entry_id", type=int)
        confirmed = request.form.get("priority_confirmed") == "on"
        db = get_db()
        entry = db.execute(
            "SELECT * FROM queue_entries WHERE id=? AND unit_id=? AND status IN ('waiting','present')",
            (entry_id, user["unit_id"]),
        ).fetchone()
        if not entry:
            flash("Paciente não encontrado na fila ativa desta unidade.", "error")
        else:
            db.execute(
                "UPDATE queue_entries SET status='present', present_at=?, priority_confirmed=? WHERE id=?",
                (now_iso(), 1 if confirmed else 0, entry_id),
            )
            notify(entry["user_id"], "Presença confirmada", "A recepção registrou sua chegada à unidade.")
            audit("confirmar_presenca", f"Presença da fila #{entry_id}; prioridade confirmada={confirmed}.", user["unit_id"])
            flash("Presença registrada. A fila foi recalculada.", "success")
        return redirect(url_for("staff_dashboard"))

    @app.post("/equipe/agendamento/presenca")
    @roles_required("receptionist", "manager")
    def checkin_appointment():
        user = current_user()
        db = get_db()
        appointment_id = request.form.get("appointment_id", type=int)
        appointment = db.execute(
            """SELECT a.*, s.unit_id, s.service, u.name AS citizen_name
               FROM appointments a JOIN slots s ON s.id=a.slot_id JOIN users u ON u.id=a.user_id
               WHERE a.id=? AND s.unit_id=? AND s.slot_date=? AND a.status='booked'""",
            (appointment_id, user["unit_id"], date.today().isoformat()),
        ).fetchone()
        if not appointment:
            flash("Agendamento não encontrado para esta unidade ou data.", "error")
            return redirect(url_for("staff_dashboard"))
        if active_queue_for_user(appointment["user_id"]):
            flash("Este cidadão já possui uma fila ativa.", "warning")
            return redirect(url_for("staff_dashboard"))
        db.execute(
            "INSERT INTO queue_entries(user_id, unit_id, service, status, created_at, present_at) VALUES(?,?,?,?,?,?)",
            (appointment["user_id"], appointment["unit_id"], appointment["service"], "present", now_iso(), now_iso()),
        )
        db.execute("UPDATE appointments SET status='checked_in', checked_in_at=? WHERE id=?", (now_iso(), appointment_id))
        notify(appointment["user_id"], "Presença confirmada", "Sua chegada para o agendamento foi registrada pela recepção.")
        audit("checkin_agendamento", f"Presença do agendamento #{appointment_id} registrada.", user["unit_id"])
        flash("Presença do agendamento registrada e paciente incluído na fila de atendimento.", "success")
        return redirect(url_for("staff_dashboard"))

    @app.post("/equipe/chamar-proximo")
    @roles_required("receptionist", "manager")
    def call_next():
        user = current_user()
        db = get_db()
        expire_calls(user["unit_id"])
        db.execute("BEGIN IMMEDIATE")
        try:
            next_entry = db.execute(
                """SELECT * FROM queue_entries WHERE unit_id=? AND status='present'
                   ORDER BY priority_confirmed DESC, created_at ASC, id ASC LIMIT 1""",
                (user["unit_id"],),
            ).fetchone()
            if not next_entry:
                db.rollback()
                flash("Não há pacientes com presença confirmada aguardando neste momento.", "info")
                return redirect(url_for("staff_dashboard"))
            updated = db.execute(
                "UPDATE queue_entries SET status='called', called_at=? WHERE id=? AND status='present'",
                (now_iso(), next_entry["id"]),
            ).rowcount
            if updated != 1:
                db.rollback()
                flash("A fila foi atualizada por outro atendente. Tente novamente.", "warning")
                return redirect(url_for("staff_dashboard"))
            db.commit()
            notify(next_entry["user_id"], "É sua vez!", "Você foi chamado. Apresente-se à recepção em até 5 minutos.")
            audit("chamar_paciente", f"Paciente da fila #{next_entry['id']} chamado.", user["unit_id"])
            flash("Próximo paciente chamado. O prazo de comparecimento é de 5 minutos.", "success")
        except Exception:
            db.rollback()
            raise
        return redirect(url_for("staff_dashboard"))

    @app.post("/equipe/iniciar/<int:entry_id>")
    @roles_required("receptionist", "manager")
    def start_attendance(entry_id: int):
        user = current_user()
        db = get_db()
        changed = db.execute(
            "UPDATE queue_entries SET status='attending', started_at=? WHERE id=? AND unit_id=? AND status='called'",
            (now_iso(), entry_id, user["unit_id"]),
        ).rowcount
        if changed:
            audit("iniciar_atendimento", f"Atendimento iniciado para fila #{entry_id}.", user["unit_id"])
            flash("Atendimento iniciado.", "success")
        else:
            flash("Não foi possível iniciar este atendimento.", "error")
        return redirect(url_for("staff_dashboard"))

    @app.post("/equipe/concluir/<int:entry_id>")
    @roles_required("receptionist", "manager")
    def complete_attendance(entry_id: int):
        user = current_user()
        db = get_db()
        entry = db.execute("SELECT * FROM queue_entries WHERE id=? AND unit_id=? AND status='attending'", (entry_id, user["unit_id"])).fetchone()
        if entry:
            db.execute("UPDATE queue_entries SET status='completed', completed_at=? WHERE id=?", (now_iso(), entry_id))
            notify(entry["user_id"], "Atendimento finalizado", "Seu atendimento foi registrado como concluído. Obrigado!")
            audit("concluir_atendimento", f"Atendimento da fila #{entry_id} concluído.", user["unit_id"])
            flash("Atendimento concluído.", "success")
        else:
            flash("Atendimento não encontrado ou já finalizado.", "error")
        return redirect(url_for("staff_dashboard"))

    @app.post("/equipe/ausente/<int:entry_id>")
    @roles_required("receptionist", "manager")
    def mark_no_show(entry_id: int):
        user = current_user()
        db = get_db()
        entry = db.execute("SELECT * FROM queue_entries WHERE id=? AND unit_id=? AND status='called'", (entry_id, user["unit_id"])).fetchone()
        if entry:
            db.execute("UPDATE queue_entries SET status='no_show' WHERE id=?", (entry_id,))
            notify(entry["user_id"], "Chamada encerrada", "A recepção registrou ausência após a chamada.")
            audit("marcar_ausente", f"Fila #{entry_id} marcada como ausente.", user["unit_id"])
            flash("Ausência registrada.", "success")
        return redirect(url_for("staff_dashboard"))

    @app.get("/gestao")
    @roles_required("manager")
    def management():
        user = current_user()
        db = get_db()
        slots = db.execute(
            """SELECT s.*, (SELECT COUNT(*) FROM appointments a WHERE a.slot_id=s.id AND a.status IN ('booked','checked_in')) AS booked
               FROM slots s WHERE s.unit_id=? AND s.slot_date>=? ORDER BY s.slot_date, s.slot_time LIMIT 80""",
            (user["unit_id"], date.today().isoformat()),
        ).fetchall()
        unit = db.execute("SELECT * FROM units WHERE id=?", (user["unit_id"],)).fetchone()
        return render_template("management.html", slots=slots, unit=unit, today=date.today().isoformat())

    @app.post("/gestao/vagas")
    @roles_required("manager")
    def create_slot():
        user = current_user()
        service = request.form.get("service", "").strip()
        slot_date = request.form.get("slot_date", "")
        slot_time = request.form.get("slot_time", "")
        capacity = request.form.get("capacity", type=int)
        try:
            parsed = date.fromisoformat(slot_date)
            valid_time = bool(re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", slot_time))
        except ValueError:
            parsed, valid_time = date.min, False
        if not service or parsed < date.today() or not valid_time or not capacity or capacity < 1 or capacity > 100:
            flash("Confira serviço, data futura, horário e capacidade (1 a 100).", "error")
        else:
            try:
                get_db().execute(
                    "INSERT INTO slots(unit_id, service, slot_date, slot_time, capacity) VALUES(?,?,?,?,?)",
                    (user["unit_id"], service, slot_date, slot_time, capacity),
                )
                audit("criar_vaga", f"Vaga criada: {service}, {slot_date} às {slot_time}, capacidade {capacity}.", user["unit_id"])
                flash("Horário disponibilizado.", "success")
            except sqlite3.IntegrityError:
                flash("Já existe um horário para este serviço, data e hora.", "warning")
        return redirect(url_for("management"))

    @app.post("/gestao/vagas/<int:slot_id>/bloquear")
    @roles_required("manager")
    def block_slot(slot_id: int):
        user = current_user()
        db = get_db()
        slot = db.execute("SELECT * FROM slots WHERE id=? AND unit_id=?", (slot_id, user["unit_id"])).fetchone()
        if not slot:
            abort(404)
        booked = db.execute("SELECT COUNT(*) FROM appointments WHERE slot_id=? AND status IN ('booked','checked_in')", (slot_id,)).fetchone()[0]
        if booked:
            flash("Não é possível bloquear: há agendamentos confirmados. Contate os cidadãos antes de alterar a vaga.", "warning")
        else:
            db.execute("UPDATE slots SET active=0 WHERE id=?", (slot_id,))
            audit("bloquear_vaga", f"Horário #{slot_id} bloqueado.", user["unit_id"])
            flash("Horário bloqueado.", "success")
        return redirect(url_for("management"))

    @app.post("/gestao/unidade")
    @roles_required("manager")
    def toggle_unit():
        user = current_user()
        db = get_db()
        unit = db.execute("SELECT is_open FROM units WHERE id=?", (user["unit_id"],)).fetchone()
        new_state = 0 if unit["is_open"] else 1
        db.execute("UPDATE units SET is_open=? WHERE id=?", (new_state, user["unit_id"]))
        audit("alterar_unidade", f"Unidade {'aberta' if new_state else 'fechada'} pelo gestor.", user["unit_id"])
        flash(f"Fila da unidade {'aberta' if new_state else 'encerrada'}.", "success")
        return redirect(url_for("management"))

    @app.get("/relatorios")
    @roles_required("manager")
    def reports():
        user = current_user()
        selected = request.args.get("data", date.today().isoformat())
        try:
            date.fromisoformat(selected)
        except ValueError:
            selected = date.today().isoformat()
        db = get_db()
        rows = db.execute(
            """SELECT status, COUNT(*) AS total FROM queue_entries
               WHERE unit_id=? AND substr(created_at,1,10)=? GROUP BY status""",
            (user["unit_id"], selected),
        ).fetchall()
        counts = {row["status"]: row["total"] for row in rows}
        avg = db.execute(
            """SELECT AVG((julianday(called_at)-julianday(created_at))*1440)
               FROM queue_entries WHERE unit_id=? AND substr(created_at,1,10)=?
                 AND called_at IS NOT NULL""",
            (user["unit_id"], selected),
        ).fetchone()[0]
        appointment_counts = db.execute(
            """SELECT a.status, COUNT(*) AS total FROM appointments a JOIN slots s ON s.id=a.slot_id
               WHERE s.unit_id=? AND s.slot_date=? GROUP BY a.status""",
            (user["unit_id"], selected),
        ).fetchall()
        ap_counts = {row["status"]: row["total"] for row in appointment_counts}
        return render_template(
            "reports.html", selected=selected, counts=counts, avg_wait=round(avg, 1) if avg else 0,
            appointment_counts=ap_counts,
        )

    @app.get("/relatorios.csv")
    @roles_required("manager")
    def reports_csv():
        user = current_user()
        selected = request.args.get("data", date.today().isoformat())
        try:
            date.fromisoformat(selected)
        except ValueError:
            abort(400)
        db = get_db()
        rows = db.execute(
            """SELECT service, status, COUNT(*) AS total FROM queue_entries
               WHERE unit_id=? AND substr(created_at,1,10)=? GROUP BY service, status ORDER BY service, status""",
            (user["unit_id"], selected),
        ).fetchall()
        output = io.StringIO()
        writer = csv.writer(output, delimiter=";")
        writer.writerow(["Data", "Serviço", "Status", "Quantidade"])
        for row in rows:
            writer.writerow([selected, row["service"], row["status"], row["total"]])
        response = make_response("\ufeff" + output.getvalue())
        response.headers["Content-Type"] = "text/csv; charset=utf-8"
        response.headers["Content-Disposition"] = f"attachment; filename=filazero-relatorio-{selected}.csv"
        return response

    @app.get("/api/minha-fila")
    @roles_required("citizen")
    def api_my_queue():
        entry = active_queue_for_user(session["user_id"])
        if not entry:
            return jsonify({"active": False})
        pos = queue_snapshot(entry["id"])
        return jsonify({
            "active": True,
            "status": entry["status"],
            "status_label": {
                "waiting": "Aguardando", "present": "Presença confirmada", "called": "Você foi chamado!",
                "attending": "Em atendimento", "completed": "Concluído",
            }.get(entry["status"], entry["status"]),
            "position": pos["position"],
            "estimated_minutes": pos["estimated_minutes"],
            "updated_at": now_iso(),
        })

    @app.errorhandler(400)
    def bad_request(error):
        return render_template("error.html", code=400, message=getattr(error, "description", "Solicitação inválida.")), 400

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("error.html", code=403, message="Seu perfil não possui permissão para acessar esta área."), 403

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("error.html", code=404, message="A página solicitada não foi encontrada."), 404

    app.get_db = get_db  # útil para testes automatizados
    app.valid_cpf = valid_cpf
    app.init_db = init_db
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=os.environ.get("FLASK_DEBUG", "0") == "1")
