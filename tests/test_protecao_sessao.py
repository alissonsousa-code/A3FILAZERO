from datetime import datetime, timedelta

from test_app import app as app, client as client, csrf, login, register_citizen


def test_post_without_csrf_is_denied_and_does_not_join_queue(app, client):
    register_citizen(client)
    login(client, 'cidadao@example.com', 'SenhaTeste@123')
    with client.session_transaction() as sess:
        assert 'user_id' in sess
    response = client.post('/fila/entrar',data={'unit_id':1,'service':'Consulta clínica'})
    assert response.status_code == 400
    with app.app_context():
        assert app.get_db().execute('SELECT COUNT(*) FROM queue_entries').fetchone()[0] == 0


def test_inactive_session_requires_login_again(client):
    register_citizen(client)
    login(client, 'cidadao@example.com', 'SenhaTeste@123')
    with client.session_transaction() as sess:
        assert 'user_id' in sess
        sess['last_seen'] = (datetime.now()-timedelta(minutes=16)).timestamp()
    response = client.get('/painel',follow_redirects=True)
    assert response.request.path == '/entrar'
    assert 'Sua sessão expirou por inatividade.' in response.get_data(as_text=True)
    with client.session_transaction() as sess:
        assert 'user_id' not in sess


def test_citizen_cannot_cancel_someone_elses_appointment(app, client):
    register_citizen(client)
    login(client, 'cidadao@example.com', 'SenhaTeste@123')
    with app.app_context():
        sid = app.get_db().execute('SELECT id FROM slots ORDER BY id LIMIT 1').fetchone()[0]
    response = client.post('/agendamentos/criar',data={'csrf_token':csrf(client),'slot_id':sid})
    assert response.status_code == 302
    with app.app_context():
        original = dict(app.get_db().execute('SELECT * FROM appointments WHERE slot_id=?',(sid,)).fetchone())
        assert original['status'] == 'booked'
        aid = original['id']
    other = app.test_client()
    register_citizen(other,'11144477735','outro@example.com')
    login(other,'outro@example.com','SenhaTeste@123')
    with other.session_transaction() as sess:
        assert sess['user_id'] != original['user_id']
    response = other.post(f'/agendamentos/cancelar/{aid}',data={'csrf_token':csrf(other)},follow_redirects=True)
    assert response.status_code == 200
    assert 'Este agendamento não pode ser cancelado.' in response.get_data(as_text=True)
    with app.app_context():
        unchanged = dict(app.get_db().execute('SELECT * FROM appointments WHERE id=?',(aid,)).fetchone())
        assert unchanged == original
