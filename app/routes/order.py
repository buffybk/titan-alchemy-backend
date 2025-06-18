from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.order import Order
from app.models.product import Product
from app.models.order_item import OrderItem
from app.models.user import User

order = Blueprint('order', __name__, url_prefix='/orders')

@order.route('/add', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        user_id = int(request.form.get('user_id'))
        products_ids = request.form.getlist('product_ids')  # Assuming the products are selected via a multi-select form
        total_price = sum([Product.query.get(int(pid)).price for pid in products_ids])

        # Create new order instance
        new_order = Order(user_id=user_id, total_price=total_price, status='pending')

        # Add order to the database
        db.session.add(new_order)
        db.session.flush()

        # Create order items and link to the order
        for pid in products_ids:
            product = Product.query.get(int(pid))
            order_item = OrderItem(order_id=new_order.id, product_id=product.id, quantity=1, unit_price=product.price)
            db.session.add(order_item)
        db.session.commit()

        flash('Order placed successfully!', 'success')
        return redirect(url_for('order.order_list'))  # Redirect to the order list

    # If GET request, fetch products for the order form
    products = Product.query.all()
    users = User.query.all()
    return render_template('order/add_order.html', products=products, users=users)


@order.route('/', methods=['GET'])
def order_list():
    # Render the list of orders
    orders = Order.query.all()
    return render_template('order/order_list.html', orders=orders)