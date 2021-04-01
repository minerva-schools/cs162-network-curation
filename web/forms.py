from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email


# from .models import User


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SignupForm(FlaskForm):
    name = StringField('First Name',
                       validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 Length(min=8,
                                        message="Your password is too short."), EqualTo('confirm_password', message='Passwords must match')
                             ])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), Length(min=8)])
    email = StringField('Email Address',
                        validators=[DataRequired(),
                                    Email(' Enter a valid email.')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')


class AddConnectionForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email Address',
                        validators=[DataRequired()])
    tag = StringField('Tag',
                      validators=[DataRequired()])
    contactby = StringField('Contact By',
                            validators=[DataRequired()])
    lastcontacted = StringField('Last Contacted',
                                validators=[DataRequired()])
    note = StringField('Note', validators=[])
    submit = SubmitField('Add Connection')
