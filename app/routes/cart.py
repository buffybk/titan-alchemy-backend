from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from app.models.product   import Product
from app.models.cart      import Cart
from app.models.cart_item import CartItem
from app.models.order     import Order
from app.models.order_item import OrderItem

cart = Blueprint('cart', __name__, url_prefix='/cart')

@cart.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    # Retrieve the current cart or create a new one if it doesn't exist
    user_cart = Cart.query.filter_by(user_id=current_user.id, status='active').first()
    if not user_cart:
        user_cart = Cart(user_id=current_user.id, status='active')
        db.session.add(user_cart)
        db.session.commit()

    # Check if the product is already in the cart
    cart_item = CartItem.query.filter_by(cart_id=user_cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        product = Product.query.get_or_404(product_id)
        cart_item = CartItem(cart_id=user_cart.id, product_id=product.id, quantity=1, unit_price=product.price)
        db.session.add(cart_item)

    db.session.commit()
    flash('Product added to cart!', 'success')
    return redirect(url_for('cart.view_cart'))

@cart.route('/view_cart')
@login_required
def view_cart():
    user_cart = Cart.query.filter_by(user_id=current_user.id, status='active').first()
    if not user_cart:
        flash('Your cart is empty', 'warning')
        return render_template('cart/empty_cart.html')

    cart_items = CartItem.query.filter_by(cart_id=user_cart.id).all()
    return render_template('cart/view_cart.html', cart=user_cart, cart_items=cart_items)

@cart.route('/remove_from_cart/<int:cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    db.session.delete(cart_item)
    db.session.commit()
    flash('Product removed from cart', 'info')
    return redirect(url_for('cart.view_cart'))

@cart.route('/update_quantity/<int:cart_item_id>', methods=['POST'])
@login_required
def update_quantity(cart_item_id):
    new_quantity = request.form.get('quantity', type=int)
    cart_item = CartItem.query.get_or_404(cart_item_id)

    if new_quantity > 0:
        cart_item.quantity = new_quantity
        db.session.commit()
        flash('Cart updated!', 'success')
    else:
        flash('Invalid quantity', 'danger')

    return redirect(url_for('cart.view_cart'))

@cart.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    user_cart = Cart.query.filter_by(user_id=current_user.id, status='active').first()
    cart_items = CartItem.query.filter_by(cart_id=user_cart.id).all() if user_cart else []
    if not user_cart or not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('cart.view_cart'))

    if request.method == 'POST':
        order = Order(user_id=current_user.id, status='pending', total_price=user_cart.total_price())
        db.session.add(order)
        db.session.flush()

        for item in cart_items:
            order_item = OrderItem(order_id=order.id,
                                   product_id=item.product_id,
                                   quantity=item.quantity,
                                   unit_price=item.unit_price)
            db.session.add(order_item)

        user_cart.status = 'completed'
        db.session.commit()

        flash('Checkout successful!', 'success')
        return redirect(url_for('order.order_history'))

    return render_template('cart/checkout.html', cart=user_cart, cart_items=cart_items)