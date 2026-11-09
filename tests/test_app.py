from datetime import date, timedelta

import pytest

from app import create_app


@pytest.fixture()
def app(tmp_path):
    database = tmp_path / "test-filazero.sqlite3"
    application = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret",
        "DATABASE": str(database),
        "DEMO_MODE": True,
    })
    with application.test_client() as client:
        client.get("/")  # inicializa esquema e token CSRF
        yield application


@pytest.fixture()
def client(app):
    return app.test_client()


def csrf(client):
    with client.session_transaction() as sess:
        return sess["csrf_token"]


def register_citizen(client, cpf="52998224725", email="cidadao@example.com"):
    client.get("/cadastro")
    return client.post("/cadastro", data={
        "csrf_token": csrf(client),
        "name": "Cidadão de Teste",
        "cpf": cpf,
        "birth_date": "1998-04-20",
        "phone": "71999990000",
        "email": email,
        "password": "SenhaTeste@123",
        "lgpd_consent": "on",
    }, follow_redirects=True)


def login(client, identifier, password):
    client.get("/entrar")
    return client.post("/entrar", data={
        "csrf_token": csrf(client),
        "identifier": identifier,
        "password": password,
    }, follow_redirects=True)


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"FilaZero" in response.data


def test_cpf_validator(app):
    assert app.valid_cpf("529.982.247-25") is True
    assert app.valid_cpf("111.111.111-11") is False
    assert app.valid_cpf("123") is False


def test_register_and_login(client):
    response = register_citizen(client)
    assert response.status_code == 200
    assert b"Cadastro conclu\xc3\xaddo" in response.data
    response = login(client, "52998224725", "SenhaTeste@123")
    assert response.status_code == 200
    assert b"Meu painel" in response.data


def test_citizen_can_join_only_one_active_queue(app, client):
    register_citizen(client)
    login(client, "cidadao@example.com", "SenhaTeste@123")
    response = client.get("/unidades")
    assert response.status_code == 200
    with app.app_context():
        db = app.get_db()
        unit_id = db.execute("SELECT id FROM units ORDER BY id LIMIT 1").fetchone()[0]
    post_data = {"csrf_token": csrf(client), "unit_id": unit_id, "service": "Consulta clínica"}
    client.post("/fila/entrar", data=post_data, follow_redirects=True)
    client.post("/fila/entrar", data=post_data, follow_redirects=True)
    with app.app_context():
        total = app.get_db().execute("SELECT COUNT(*) FROM queue_entries").fetchone()[0]
    assert total == 1


def test_manager_area_is_forbidden_to_citizen(client):
    register_citizen(client)
    login(client, "cidadao@example.com", "SenhaTeste@123")
    response = client.get("/gestao")
    assert response.status_code == 403


def test_booking_respects_slot_capacity(app, client):
    register_citizen(client)
    login(client, "cidadao@example.com", "SenhaTeste@123")
    with app.app_context():
        db = app.get_db()
        unit_id = db.execute("SELECT id FROM units ORDER BY id LIMIT 1").fetchone()[0]
        slot_date = (date.today() + timedelta(days=10)).isoformat()
        db.execute(
            "INSERT INTO slots(unit_id, service, slot_date, slot_time, capacity) VALUES(?,?,?,?,1)",
            (unit_id, "Teste de capacidade", slot_date, "16:30"),
        )
        slot_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    response = client.post("/agendamentos/criar", data={"csrf_token": csrf(client), "slot_id": slot_id}, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        booked = app.get_db().execute(
            "SELECT COUNT(*) FROM appointments WHERE slot_id=? AND status='booked'", (slot_id,)
        ).fetchone()[0]
    assert booked == 1


def test_priority_confirmed_patient_is_called_first(app, client):
    register_citizen(client, "52998224725", "comum@example.com")
    register_citizen(client, "11144477735", "prioritario@example.com")
    with app.app_context():
        db = app.get_db()
        unit_id = db.execute("SELECT id FROM units ORDER BY id LIMIT 1").fetchone()[0]
        common_id = db.execute("SELECT id FROM users WHERE email='comum@example.com'").fetchone()[0]
        priority_id = db.execute("SELECT id FROM users WHERE email='prioritario@example.com'").fetchone()[0]
        db.execute(
            "INSERT INTO queue_entries(user_id,unit_id,service,priority_declared,priority_confirmed,status,created_at) VALUES(?,?,?,?,?,?,?)",
            (common_id, unit_id, "Consulta clínica", 0, 0, "present", "2026-11-06T08:00:00"),
        )
        db.execute(
            "INSERT INTO queue_entries(user_id,unit_id,service,priority_declared,priority_confirmed,status,created_at) VALUES(?,?,?,?,?,?,?)",
            (priority_id, unit_id, "Consulta clínica", 1, 1, "present", "2026-11-06T08:05:00"),
        )
    login(client, "recepcao@filazero.local", "Recepcao@123")
    client.post("/equipe/chamar-proximo", data={"csrf_token": csrf(client)}, follow_redirects=True)
    with app.app_context():
        called_user = app.get_db().execute(
            "SELECT user_id FROM queue_entries WHERE status='called'"
        ).fetchone()[0]
    assert called_user == priority_id


def test_slot_capacity_rejects_second_citizen(app, client):
    register_citizen(client, "52998224725", "primeiro@example.com")
    with app.app_context():
        db = app.get_db()
        unit_id = db.execute("SELECT id FROM units ORDER BY id LIMIT 1").fetchone()[0]
        slot_date = (date.today() + timedelta(days=10)).isoformat()
        db.execute(
            "INSERT INTO slots(unit_id, service, slot_date, slot_time, capacity) VALUES(?,?,?,?,1)",
            (unit_id, "Vaga unitária", slot_date, "17:00"),
        )
        slot_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    login(client, "primeiro@example.com", "SenhaTeste@123")
    client.post("/agendamentos/criar", data={"csrf_token": csrf(client), "slot_id": slot_id}, follow_redirects=True)

    second_client = app.test_client()
    register_citizen(second_client, "11144477735", "segundo@example.com")
    login(second_client, "segundo@example.com", "SenhaTeste@123")
    second_client.post("/agendamentos/criar", data={"csrf_token": csrf(second_client), "slot_id": slot_id}, follow_redirects=True)
    with app.app_context():
        booked = app.get_db().execute(
            "SELECT COUNT(*) FROM appointments WHERE slot_id=? AND status='booked'", (slot_id,)
        ).fetchone()[0]
    assert booked == 1
