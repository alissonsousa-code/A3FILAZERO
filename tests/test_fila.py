from test_app import app as app, client as client, csrf, login, register_citizen


def join(client, unit_id=1, priority=False):
    return client.post('/fila/entrar', data={
        'csrf_token': csrf(client),
        'unit_id': unit_id,
        'service': 'Consulta clínica',
        'priority_declared': 'on' if priority else '',
    }, follow_redirects=True)


def queue_state(app, entry_id):
    with app.app_context():
        return app.get_db().execute(
            'SELECT status FROM queue_entries WHERE id=?', (entry_id,),
        ).fetchone()[0]


def test_closed_unit_refuses_queue_entry(app, client):
    register_citizen(client)
    login(client, 'cidadao@example.com', 'SenhaTeste@123')
    with app.app_context():
        app.get_db().execute('UPDATE units SET is_open=0 WHERE id=1')

    response = join(client)

    assert response.status_code == 200
    assert 'A fila desta unidade está encerrada' in response.get_data(as_text=True)
    with app.app_context():
        assert app.get_db().execute('SELECT COUNT(*) FROM queue_entries').fetchone()[0] == 0


def test_declared_priority_alone_does_not_jump_the_queue(app, client):
    register_citizen(client)
    login(client, 'cidadao@example.com', 'SenhaTeste@123')
    assert join(client).status_code == 200

    other = app.test_client()
    register_citizen(other, '11144477735', 'outro@example.com')
    login(other, 'outro@example.com', 'SenhaTeste@123')
    assert join(other, priority=True).status_code == 200
    with app.app_context():
        rows = app.get_db().execute('SELECT * FROM queue_entries ORDER BY id').fetchall()
        assert len(rows) == 2
        first_id, declared_id = [row['id'] for row in rows]
        assert rows[1]['priority_declared'] == 1
        assert rows[1]['priority_confirmed'] == 0

    reception = app.test_client()
    login(reception, 'recepcao@filazero.local', 'Recepcao@123')
    for entry_id in (first_id, declared_id):
        response = reception.post('/equipe/presenca', data={
            'csrf_token': csrf(reception), 'entry_id': entry_id,
        })
        assert response.status_code == 302
        assert queue_state(app, entry_id) == 'present'
    response = reception.post('/equipe/chamar-proximo', data={'csrf_token': csrf(reception)})

    assert response.status_code == 302
    assert queue_state(app, first_id) == 'called'
    assert queue_state(app, declared_id) == 'present'


def test_attendance_follows_presence_call_start_and_completion(app, client):
    register_citizen(client)
    login(client, 'cidadao@example.com', 'SenhaTeste@123')
    assert join(client).status_code == 200
    with app.app_context():
        entry_id = app.get_db().execute('SELECT id FROM queue_entries').fetchone()[0]
    reception = app.test_client()
    login(reception, 'recepcao@filazero.local', 'Recepcao@123')

    def post(path, **data):
        response = reception.post(path, data={'csrf_token': csrf(reception), **data})
        assert response.status_code == 302

    post(f'/equipe/iniciar/{entry_id}')
    assert queue_state(app, entry_id) == 'waiting'
    post('/equipe/presenca', entry_id=entry_id)
    assert queue_state(app, entry_id) == 'present'
    post(f'/equipe/iniciar/{entry_id}')
    assert queue_state(app, entry_id) == 'present'
    post('/equipe/chamar-proximo')
    assert queue_state(app, entry_id) == 'called'
    post(f'/equipe/concluir/{entry_id}')
    assert queue_state(app, entry_id) == 'called'
    post(f'/equipe/iniciar/{entry_id}')
    assert queue_state(app, entry_id) == 'attending'
    post(f'/equipe/concluir/{entry_id}')
    assert queue_state(app, entry_id) == 'completed'


def test_citizen_can_rejoin_after_cancelling_queue(app, client):
    register_citizen(client)
    login(client, 'cidadao@example.com', 'SenhaTeste@123')
    assert join(client).status_code == 200
    with app.app_context():
        old_id = app.get_db().execute('SELECT id FROM queue_entries').fetchone()[0]
    response = client.post(f'/fila/cancelar/{old_id}', data={'csrf_token': csrf(client)})
    assert response.status_code == 302
    assert queue_state(app, old_id) == 'cancelled'

    assert join(client).status_code == 200

    with app.app_context():
        rows = app.get_db().execute('SELECT id,status FROM queue_entries ORDER BY id').fetchall()
        assert len(rows) == 2
        assert [(row['id'], row['status']) for row in rows] == [
            (old_id, 'cancelled'), (rows[1]['id'], 'waiting'),
        ]
        assert rows[1]['id'] != old_id
