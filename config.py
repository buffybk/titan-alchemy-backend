import os
from dotenv import load_dotenv # type: ignore

# Load environment variables from a .env file (optional but nice to have)
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'app.db')
    )
    DEBUG = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    DEBUG = False

# Auto-select config based on FLASK_ENV
config = ProductionConfig if os.getenv('FLASK_ENV') == 'production' else DevelopmentConfig