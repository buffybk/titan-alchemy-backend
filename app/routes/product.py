from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models.product import Product

# Create a Blueprint for the product routes
product = Blueprint('product', __name__, url_prefix='/product')

@product.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        image_url = request.form.get('image_url')

        # Create new product instance
        new_product = Product(
            name=name,
            description=description,
            price=float(price),
            image_url=image_url
        )

        # Add product to the database
        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully!', 'success')
        return redirect(url_for('product.product_list'))

    # If GET request, render the form
    return render_template('product/add_product.html')


@product.route('/product_list')
def product_list():
    # Fetch all products
    products = Product.query.all()
    return render_template('product/product_list.html', products=products)

@product.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image_url': product.image_url,
        'category': product.category
    })