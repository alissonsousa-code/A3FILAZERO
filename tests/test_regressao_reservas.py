"""Reproduções isoladas de DEF01/DEF02; xfail não representa aprovação.

Os marcadores estritos são ativados somente depois de validar a preparação.
Quando a correção entrar, XPASS falha e exige retirar o marcador do caso corrigido.
"""

import sqlite3
from datetime import date, timedelta

import pytest

from test_app import app as app, client as client, csrf, login, register_citizen


def create_single_slot(app, slot_date):
    with app.app_context():
        db = app.get_db()
        db.execute(
            'INSERT INTO slots(unit_id,service,slot_date,slot_time,capacity) VALUES(1,?,?,?,1)',
            ('Regressão de reservas', slot_date.isoformat(), '23:50'),
        )
        return db.execute('SELECT last_insert_rowid()').fetchone()[0]


def test_cancelled_appointment_can_be_booked_again(app, client, request):
    register_citizen(client)
    login(client, 'cidadao@example.com', 'SenhaTeste@123')
    slot_id = create_single_slot(app, date.today() + timedelta(days=10))
    response = client.post('/agendamentos/criar', data={'csrf_token': csrf(client), 'slot_id': slot_id})
    assert response.status_code == 302
    with app.app_context():
        appointment_id = app.get_db().execute(
            'SELECT id FROM appointments WHERE slot_id=?', (slot_id,),
        ).fetchone()[0]
    response = client.post(f'/agendamentos/cancelar/{appointment_id}', data={'csrf_token': csrf(client)})
    assert response.status_code == 302
    with app.app_context():
        assert app.get_db().execute(
            'SELECT status FROM appointments WHERE id=?', (appointment_id,),
        ).fetchone()[0] == 'cancelled'

    request.applymarker(pytest.mark.xfail(
        strict=True, raises=sqlite3.IntegrityError,
        reason='DEF01: UNIQUE(user_id, slot_id) impede reservar de novo após cancelar',
    ))
    response = client.post('/agendamentos/criar', data={
        'csrf_token': csrf(client), 'slot_id': slot_id,
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Agendamento confirmado!' in response.get_data(as_text=True)
    with app.app_context():
        states = [row[0] for row in app.get_db().execute(
            'SELECT status FROM appointments WHERE slot_id=? ORDER BY id', (slot_id,),
        )]
        assert states == ['cancelled', 'booked']


def test_checkin_keeps_capacity_occupied(app, client, request):
    register_citizen(client)
    login(client, 'cidadao@example.com', 'SenhaTeste@123')
    slot_id = create_single_slot(app, date.today())
    response = client.post('/agendamentos/criar', data={'csrf_token': csrf(client), 'slot_id': slot_id})
    assert response.status_code == 302
    with app.app_context():
        appointment_id = app.get_db().execute(
            'SELECT id FROM appointments WHERE slot_id=?', (slot_id,),
        ).fetchone()[0]
    reception = app.test_client()
    login(reception, 'recepcao@filazero.local', 'Recepcao@123')
    response = reception.post('/equipe/agendamento/presenca', data={
        'csrf_token': csrf(reception), 'appointment_id': appointment_id,
    })
    assert response.status_code == 302
    with app.app_context():
        assert app.get_db().execute(
            'SELECT status FROM appointments WHERE id=?', (appointment_id,),
        ).fetchone()[0] == 'checked_in'

    other = app.test_client()
    register_citizen(other, '11144477735', 'outro@example.com')
    login(other, 'outro@example.com', 'SenhaTeste@123')
    response = other.post('/agendamentos/criar', data={
        'csrf_token': csrf(other), 'slot_id': slot_id,
    }, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        states = [row[0] for row in app.get_db().execute(
            'SELECT status FROM appointments WHERE slot_id=? ORDER BY id', (slot_id,),
        )]
    request.applymarker(pytest.mark.xfail(
        strict=True, raises=AssertionError,
        reason='DEF02: check-in deixa de contar na capacidade e permite uma segunda reserva',
    ))
    assert states == ['checked_in'], f'Capacidade=1; estados observados: {states}'
    assert 'A vaga foi ocupada' in response.get_data(as_text=True)
