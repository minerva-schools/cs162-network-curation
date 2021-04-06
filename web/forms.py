from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField, TelField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp, ValidationError

import datetime


class LoginForm(FlaskForm):
    email_or_username = StringField('Email Address or Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SignupForm(FlaskForm):
    user_name = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^\w+$',
                message="Username must contain only letters, numbers or underscore"
            ),
            Length(
                min=5,
                max=25,
                message="Username must be between 5 & 25 characters"
            )
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(
                min=8,
                message="Your password must have at least 8 characters"
            ),
            EqualTo(
                'confirm_password',
                message='Passwords must match'
            )
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(),
            Email('Enter a valid email')
        ]
    )
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')


class AddConnectionForm(FlaskForm):
    name = StringField(
        'Full Name',
        validators=[DataRequired()]
    )
    title = StringField('Title')
    phone = TelField('Phone')
    email = EmailField(
        'Email Address',
        validators=[Email('Enter a valid email')]
    )
    tags = StringField('Tags')
    contact_by = DateField(
        'Contact By',
        format='%Y-%m-%d',
    )
    last_contacted = DateField(
        'Last Contacted',
        format='%Y-%m-%d',
    )
    note = TextAreaField('Note')
    submit = SubmitField('Add Connection')
