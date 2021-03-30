from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


# from .models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SignupForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=4, message="Your username is too short.")])
    name = StringField('Full Name',
                           validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 Length(min=8,
                                        message="Your password is too short.")
                             ])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message="Passwords are not equal.")])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email Address',
                        validators=[DataRequired(),
                                    Length(min=6, message='Your email is too short.')])
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
