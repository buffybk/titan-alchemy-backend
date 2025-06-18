# app/forms.py

from flask_wtf import FlaskForm  # type: ignore
from wtforms import StringField, PasswordField, SubmitField  # type: ignore
from wtforms.validators import DataRequired, Email, Length, EqualTo  # type: ignore

# Form for user login
class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Log In')

# Form for user registration
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')