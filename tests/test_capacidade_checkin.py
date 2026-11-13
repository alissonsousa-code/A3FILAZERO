from datetime import date

from test_app import app as app, client as client, csrf, login, register_citizen


def test_checkin_does_not_release_last_slot(app, client):
    register_citizen(client)
    login(client, 'cidadao@example.com', 'SenhaTeste@123')
    with app.app_context():
        db = app.get_db()
        db.execute("INSERT INTO slots(unit_id,service,slot_date,slot_time,capacity) VALUES(1,'Consulta clínica',?,'23:50',1)", (date.today().isoformat(),))
        sid = db.execute('SELECT last_insert_rowid()').fetchone()[0]
    client.post('/agendamentos/criar', data={'csrf_token':csrf(client),'slot_id':sid})
    with app.app_context():
        aid = app.get_db().execute('SELECT id FROM appointments WHERE slot_id=?',(sid,)).fetchone()[0]
    reception = app.test_client()
    login(reception, 'recepcao@filazero.local', 'Recepcao@123')
    reception.post('/equipe/agendamento/presenca', data={'csrf_token':csrf(reception),'appointment_id':aid})
    other = app.test_client()
    register_citizen(other, '11144477735', 'segundo@example.com')
    login(other, 'segundo@example.com', 'SenhaTeste@123')
    response = other.post('/agendamentos/criar', data={'csrf_token':csrf(other),'slot_id':sid}, follow_redirects=True)
    assert 'A vaga foi ocupada' in response.get_data(as_text=True)
    with app.app_context():
        states = [r[0] for r in app.get_db().execute('SELECT status FROM appointments WHERE slot_id=?',(sid,))]
    assert states == ['checked_in']
    manager = app.test_client()
    login(manager, 'gestor@filazero.local', 'Gestor@123')
    response = manager.post(f'/gestao/vagas/{sid}/bloquear',data={'csrf_token':csrf(manager)},follow_redirects=True)
    assert 'Não é possível bloquear' in response.get_data(as_text=True)
    with app.app_context():
        assert app.get_db().execute('SELECT active FROM slots WHERE id=?',(sid,)).fetchone()[0] == 1
