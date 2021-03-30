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
                                       Length(min=4, max=25)])
    name = StringField('Full Name',
                           validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email Address',
                        validators=[DataRequired(),
                                    Length(min=6, max=35)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')


class AddConnectionForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email Address',
                        validators=[DataRequired()])
    submit = SubmitField('Add Connection')
