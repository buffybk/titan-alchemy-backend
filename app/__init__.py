from flask import Flask, send_from_directory, jsonify # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_login import LoginManager # type: ignore
from config import config
import os
from flask_migrate import Migrate
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config)
    # Override DB URI if set in environment
    db_uri = os.environ.get('SQLALCHEMY_DATABASE_URI')
    if db_uri:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    # Register Blueprints
    from app.routes import main, auth, product, cart, order
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(product)
    app.register_blueprint(cart)
    app.register_blueprint(order)

    # Import all models so Flask-Migrate (Alembic) can detect them
    with app.app_context():
        from app.models.user import User
        from app.models.product import Product
        from app.models.order import Order
        from app.models.cart_item import CartItem
        from app.models.cart import Cart
        from app.models.payment import Payment
        from app.models.address import Address

    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy"}), 200

    return app