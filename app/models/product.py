from datetime import datetime
from app import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(250), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_items = db.relationship('OrderItem', back_populates='product', lazy='dynamic', cascade="all, delete-orphan")
    cart_items = db.relationship('CartItem', back_populates='product', lazy='dynamic', cascade="all, delete-orphan")
    category = db.Column(db.String(80), nullable=False, default="Other")

    def __repr__(self):
        return f'<Product {self.name}>'