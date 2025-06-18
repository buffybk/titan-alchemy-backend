from app import db
from app.models.user import User


class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)

    # Relationship back to User
    user = db.relationship('User', back_populates='addresses', passive_deletes=True)

    def __repr__(self):
        return f'<Address {self.id} for User {self.user_id}>'
