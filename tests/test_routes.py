import pytest
from app import create_app
from app.models import db, User, Product
from flask_login import current_user

@pytest.fixture
def app():
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_catalog_api(client):
    response = client.get('/api/catalog')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = response.get_json()
    assert isinstance(data, list)

def test_register_user(client):
    response = client.post('/api/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    assert response.status_code == 200
    assert User.query.filter_by(username='testuser').first() is not None

def test_login_user(client):
    # First register a user
    client.post('/api/register', json={
        'username': 'logintest',
        'email': 'login@example.com',
        'password': 'testpass123'
    })
    
    # Then try to login
    response = client.post('/api/login', json={
        'email': 'login@example.com',
        'password': 'testpass123'
    })
    assert response.status_code == 200
    assert response.get_json().get('message') == 'Logged in successfully' 