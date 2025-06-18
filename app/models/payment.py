

from datetime import datetime
from app import db

class Payment(db.Model):
    __tablename__ = 'payments'

    id        = db.Column(db.Integer, primary_key=True)
    order_id  = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount    = db.Column(db.Numeric(10, 2), nullable=False)
    paid_at   = db.Column(db.DateTime, default=datetime.utcnow)

    # relationship back to the Order
    order     = db.relationship('Order', back_populates='payment')