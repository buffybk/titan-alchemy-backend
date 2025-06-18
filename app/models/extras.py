from app import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.now())
    payment_status = db.Column(db.String(20), default='pending')

    order = db.relationship('Order', backref=db.backref('payment', uselist=False))

 
class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    address_line_1 = db.Column(db.String(100), nullable=False)
    address_line_2 = db.Column(db.String(100))
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50))
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(50), nullable=False)

    user = db.relationship('User', backref=db.backref('addresses', lazy=True))


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500))
    review_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    product = db.relationship('Product', backref=db.backref('reviews', lazy=True))
