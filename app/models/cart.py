from app import db

class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='active')

    user = db.relationship('User', back_populates='carts')
    cart_items = db.relationship(
        'CartItem',
        back_populates='cart',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    def total_price(self):
        return sum(item.quantity * item.unit_price for item in self.cart_items)

    def __repr__(self):
        return f'<Cart id={self.id} user_id={self.user_id} status={self.status}>'