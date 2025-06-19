import pytest
from app import create_app, db
from app.models import User, Product
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

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}

def test_register_user(client):
    response = client.post('/register', json={
        'email': 'test@example.com',
        'password': 'testpass123',
        'firstName': 'Test',
        'lastName': 'User'
    })
    assert response.status_code == 200
    assert response.get_json().get('success') is True
    user = User.query.filter_by(email='test@example.com').first()
    assert user is not None
    assert user.firstName == 'Test'
    assert user.lastName == 'User'

def test_login_user(client):
    # First register a user
    client.post('/register', json={
        'email': 'login@example.com',
        'password': 'testpass123',
        'firstName': 'Login',
        'lastName': 'Test'
    })
    
    # Then try to login
    response = client.post('/login', json={
        'email': 'login@example.com',
        'password': 'testpass123'
    })
    assert response.status_code == 200
    assert response.get_json().get('success') is True 