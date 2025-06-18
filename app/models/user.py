from app import db
from flask_login import UserMixin # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(80), unique=True, nullable=False)  # Removed
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstName = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationship to orders
    orders = db.relationship(
        'Order',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    # Relationship to carts
    carts = db.relationship(
        'Cart',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    # Relationship to addresses
    addresses = db.relationship(
        'Address',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<User {self.username}>'

    # Set hashed password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check hashed password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)