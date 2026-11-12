from test_app import app as app, client as client, csrf, login, register_citizen


def test_call_next_skips_citizen_without_presence(app, client):
    register_citizen(client)
    with app.app_context():
        db = app.get_db()
        uid = db.execute("SELECT id FROM users WHERE email='cidadao@example.com'").fetchone()[0]
        db.execute("INSERT INTO queue_entries(user_id,unit_id,service,status,created_at) VALUES(?,1,'Consulta clínica','waiting','2026-11-09T08:00:00')", (uid,))
    login(client, 'recepcao@filazero.local', 'Recepcao@123')
    client.post('/equipe/chamar-proximo', data={'csrf_token': csrf(client)})
    with app.app_context():
        state = app.get_db().execute('SELECT status FROM queue_entries WHERE user_id=?', (uid,)).fetchone()[0]
    assert state == 'waiting'


def test_call_next_selects_present_even_if_waiting_entered_first(app, client):
    register_citizen(client)
    register_citizen(client, '11144477735', 'presente@example.com')
    with app.app_context():
        db = app.get_db()
        for email, state, time in [('cidadao@example.com', 'waiting', '08:00:00'), ('presente@example.com', 'present', '08:05:00')]:
            uid = db.execute('SELECT id FROM users WHERE email=?', (email,)).fetchone()[0]
            db.execute('INSERT INTO queue_entries(user_id,unit_id,service,status,created_at) VALUES(?,1,?,?,?)', (uid, 'Consulta clínica', state, '2026-11-09T'+time))
    login(client, 'recepcao@filazero.local', 'Recepcao@123')
    client.post('/equipe/chamar-proximo', data={'csrf_token': csrf(client)})
    with app.app_context():
        rows = app.get_db().execute('SELECT u.email,q.status FROM queue_entries q JOIN users u ON u.id=q.user_id').fetchall()
        result = {r['email']:r['status'] for r in rows}
    assert result['presente@example.com'] == 'called'
    assert result['cidadao@example.com'] == 'waiting'
