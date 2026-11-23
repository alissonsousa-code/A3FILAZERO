from datetime import date

from test_app import app as app, client as client, csrf, login, register_citizen


def _slot(app, capacity=1):
    with app.app_context():
        db = app.get_db()
        db.execute(
            "INSERT INTO slots(unit_id,service,slot_date,slot_time,capacity) VALUES(1,'Consulta clínica',?,'23:55',?)",
            (date.today().isoformat(), capacity),
        )
        return db.execute('SELECT last_insert_rowid()').fetchone()[0]


def test_rebook_after_cancel_keeps_history(app, client):
    register_citizen(client)
    login(client, 'cidadao@example.com', 'SenhaTeste@123')
    sid = _slot(app)
    client.post('/agendamentos/criar', data={'csrf_token': csrf(client), 'slot_id': sid})
    with app.app_context():
        aid = app.get_db().execute('SELECT id FROM appointments WHERE slot_id=?', (sid,)).fetchone()[0]
    client.post(f'/agendamentos/cancelar/{aid}', data={'csrf_token': csrf(client)})
    response = client.post('/agendamentos/criar', data={'csrf_token': csrf(client), 'slot_id': sid},
                           follow_redirects=True)
    assert response.status_code == 200
    assert 'Agendamento confirmado' in response.get_data(as_text=True)
    with app.app_context():
        states = sorted(r[0] for r in app.get_db().execute('SELECT status FROM appointments WHERE slot_id=?', (sid,)))
    assert states == ['booked', 'cancelled']


def test_same_person_cannot_hold_two_active_bookings(app, client):
    register_citizen(client)
    login(client, 'cidadao@example.com', 'SenhaTeste@123')
    sid = _slot(app, capacity=3)
    client.post('/agendamentos/criar', data={'csrf_token': csrf(client), 'slot_id': sid})
    response = client.post('/agendamentos/criar', data={'csrf_token': csrf(client), 'slot_id': sid},
                           follow_redirects=True)
    assert 'você já possui reserva' in response.get_data(as_text=True)
    with app.app_context():
        total = app.get_db().execute('SELECT COUNT(*) FROM appointments WHERE slot_id=?', (sid,)).fetchone()[0]
    assert total == 1
