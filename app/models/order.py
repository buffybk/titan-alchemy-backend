# app/models/order.py
from app import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    total = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now()
    )

    # Relationship back to the User model
    user = db.relationship(
        'User',
        back_populates='orders',
        passive_deletes=True
    )

    # One-to-many: this order's items
    order_items = db.relationship(
        'OrderItem',
        back_populates='order',
        cascade='all, delete-orphan',
        passive_deletes=True,
        lazy='dynamic'
    )

    payment = db.relationship(
        'Payment',
        back_populates='order',
        uselist=False,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Order {self.id} by User {self.user_id}>'