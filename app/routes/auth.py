# app/routes/.py

from flask import Blueprint, redirect, url_for, flash, request, jsonify, render_template
from flask_login import login_user, logout_user, login_required, current_user 
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User
from app.forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return jsonify({'success': True, 'redirect': url_for('main.after_login')})
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
    else:
        return jsonify({'success': False, 'message': 'Invalid request'}), 400

@auth.route('/register', methods=['POST'])
@auth.route('/register/', methods=['POST'])
def register():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            # username = data.get('username')  # Removed
            email = data.get('email')
            password = data.get('password')
            firstName = data.get('firstName')
            lastName = data.get('lastName')
            
            # Check if user already exists (by email only)
            if User.query.filter(User.email == email).first():
                return jsonify({'success': False, 'message': 'User already exists.'}), 409
            
            # Create new user
            user = User(
                email=email,
                firstName=firstName,
                lastName=lastName
            )
            user.set_password(password)
            
            try:
                db.session.add(user)
        db.session.commit()
                return jsonify({
                    'success': True,
                    'message': 'Registration successful! Please log in.'
                })
            except Exception as e:
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'message': 'An error occurred during registration.'
                }), 500
        else:
            return jsonify({'success': False, 'message': 'Invalid request format'}), 400
    return jsonify({'success': False, 'message': 'Method not allowed'}), 405

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'success': True, 'message': 'You have been logged out.'})