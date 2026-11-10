from test_app import app as app, client as client


def test_not_found_shows_actionable_title_and_home_link(client):
    response = client.get('/pagina-inexistente')
    assert response.status_code == 404
    page = response.get_data(as_text=True)
    assert 'Página não encontrada' in page
    assert 'role="alert"' in page
    assert 'Voltar ao início' in page


def test_bad_csrf_shows_actionable_title(client):
    client.get('/entrar')
    response = client.post('/entrar', data={})
    assert response.status_code == 400
    assert 'Confira os dados enviados' in response.get_data(as_text=True)
