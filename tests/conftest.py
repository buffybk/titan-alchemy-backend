import pytest
from app import create_app, db
import os

@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    
    # Configure the app for testing
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False
    })

    # Create the database and context
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(scope='function')
def init_database(app):
    # Create the database and the database tables
    with app.app_context():
        db.create_all()
    
    yield db  # this is where the testing happens
    
    # Tear down the database
    with app.app_context():
        db.session.remove()
        db.drop_all() 