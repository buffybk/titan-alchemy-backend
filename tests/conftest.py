import pytest
import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

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
        from app import db
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
        from app import db
        db.create_all()
    
    yield db  # this is where the testing happens
    
    # Tear down the database
    with app.app_context():
        from app import db
        db.session.remove()
        db.drop_all() 