from flask import Blueprint, jsonify, current_app, send_from_directory, render_template
import os
from app import db
from app.models import User, Product, Order  # Make sure these are defined properly

# Create a Blueprint for the main routes
main = Blueprint('main', __name__)

@main.route('/users')
def list_users():
    # Fetch all users and return JSON
    users = User.query.all()
    return jsonify([
        {"id": user.id, "username": user.username, "email": user.email}
        for user in users
    ])

@main.route('/products')
def list_products():
    # Fetch all products and return JSON
    products = Product.query.all()
    return jsonify([
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "image_url": product.image_url,
            "category": product.category
        }
        for product in products
    ])

@main.route('/orders')
def list_orders():
    # Fetch all orders and return JSON
    orders = Order.query.all()
    return jsonify([
        {"id": order.id, "user_id": order.user_id, "total": order.total}
        for order in orders
    ])

@main.route('/after_login')
def after_login():
    return render_template('after_login.html')

@main.route('/debug/users')
def debug_users():
    from app.models import User
    return jsonify([
        {'id': u.id, 'username': u.username, 'email': u.email}
        for u in User.query.all()
    ])