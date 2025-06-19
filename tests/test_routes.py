import pytest
import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

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

def test_register_user(client, app):
    with app.app_context():
        from app import db
        from app.models import User
        
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

def test_login_user(client, app):
    with app.app_context():
        from app import db
        from app.models import User
        
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

def test_app_creation():
    """Test that the app can be created."""
    app = create_app('testing')
    assert app is not None
    assert app.config['TESTING'] is True 