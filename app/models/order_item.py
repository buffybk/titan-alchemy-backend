from app import db

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id', ondelete='CASCADE'),
        nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship(
        'Order',
        back_populates='order_items',
        passive_deletes=True
    )
    product = db.relationship(
        'Product',
        back_populates='order_items',
        passive_deletes=True
    )

    def __repr__(self):
        return (
            f'<OrderItem id={self.id} '
            f'order_id={self.order_id} product_id={self.product_id} '
            f'qty={self.quantity} unit_price={self.unit_price}>'
        )
