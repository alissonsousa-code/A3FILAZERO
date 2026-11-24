import pytest

from test_app import app as app, client as client, csrf, login, register_citizen


def test_wrong_csrf_token_cannot_change_queue(app, client):
    register_citizen(client)
    login(client, 'cidadao@example.com', 'SenhaTeste@123')

    response = client.post('/fila/entrar', data={
        'csrf_token': csrf(client) + '-alterado', 'unit_id': 1, 'service': 'Consulta clínica',
    })

    assert response.status_code == 400
    with app.app_context():
        assert app.get_db().execute('SELECT COUNT(*) FROM queue_entries').fetchone()[0] == 0


def test_citizen_cannot_cancel_someone_elses_queue(app, client):
    register_citizen(client)
    login(client, 'cidadao@example.com', 'SenhaTeste@123')
    response = client.post('/fila/entrar', data={
        'csrf_token': csrf(client), 'unit_id': 1, 'service': 'Consulta clínica',
    })
    assert response.status_code == 302
    with app.app_context():
        original = dict(app.get_db().execute('SELECT * FROM queue_entries').fetchone())

    other = app.test_client()
    register_citizen(other, '11144477735', 'outro@example.com')
    login(other, 'outro@example.com', 'SenhaTeste@123')
    with other.session_transaction() as sess:
        assert sess['user_id'] != original['user_id']
    response = other.post(f"/fila/cancelar/{original['id']}", data={
        'csrf_token': csrf(other),
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Esta fila não pode mais ser cancelada.' in response.get_data(as_text=True)
    with app.app_context():
        unchanged = dict(app.get_db().execute('SELECT * FROM queue_entries').fetchone())
        assert unchanged == original


@pytest.mark.parametrize('operation', ['chamar-proximo', 'presenca', 'iniciar', 'concluir'])
def test_citizen_cannot_execute_staff_actions(app, client, operation):
    register_citizen(client)
    login(client, 'cidadao@example.com', 'SenhaTeste@123')
    with client.session_transaction() as sess:
        user_id = sess['user_id']
    with app.app_context():
        db = app.get_db()
        db.execute(
            "INSERT INTO queue_entries(user_id,unit_id,service,status,created_at) VALUES(?,1,?,'present',?)",
            (user_id, 'Consulta clínica', '2026-11-13T08:00:00'),
        )
        original = dict(db.execute('SELECT * FROM queue_entries').fetchone())
    path = f'/equipe/{operation}'
    if operation in ('iniciar', 'concluir'):
        path += f"/{original['id']}"

    response = client.post(path, data={'csrf_token': csrf(client), 'entry_id': original['id']})

    assert response.status_code == 403
    with app.app_context():
        assert dict(app.get_db().execute('SELECT * FROM queue_entries').fetchone()) == original


def test_receptionist_cannot_change_queue_from_another_unit(app, client):
    register_citizen(client)
    with app.app_context():
        db = app.get_db()
        user_id = db.execute("SELECT id FROM users WHERE email='cidadao@example.com'").fetchone()[0]
        reception_unit = db.execute(
            "SELECT unit_id FROM users WHERE email='recepcao@filazero.local'",
        ).fetchone()[0]
        other_unit = db.execute('SELECT id FROM units WHERE id!=? ORDER BY id', (reception_unit,)).fetchone()[0]
        db.execute(
            "INSERT INTO queue_entries(user_id,unit_id,service,status,created_at) VALUES(?,?,?,'waiting',?)",
            (user_id, other_unit, 'Consulta clínica', '2026-11-13T08:00:00'),
        )
        original = dict(db.execute('SELECT * FROM queue_entries').fetchone())
    login(client, 'recepcao@filazero.local', 'Recepcao@123')

    response = client.post('/equipe/presenca', data={
        'csrf_token': csrf(client), 'entry_id': original['id'], 'priority_confirmed': 'on',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Paciente não encontrado na fila ativa desta unidade.' in response.get_data(as_text=True)
    with app.app_context():
        assert dict(app.get_db().execute('SELECT * FROM queue_entries').fetchone()) == original
