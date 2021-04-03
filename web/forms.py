from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp


from .models import User


class LoginForm(FlaskForm):
    email_or_username = StringField('Email Address or Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SignupForm(FlaskForm):
    user_name = StringField('Username',
                       validators=[DataRequired(), Regexp('^\w+$', message="Username must contain only letters, numbers or underscore"), Length(min=5, max=25, message="Username must be between 5 & 25 characters")])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 Length(min=8,
                                        message="Your password must have at least 8 characters"), EqualTo('confirm_password', message='Passwords must match')
                             ])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), Length(min=8)])
    email = StringField('Email Address',
                        validators=[DataRequired(),
                                    Email('Enter a valid email')])
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

class RequestResetForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    submit = SubmitField('Request Password Reset')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 Length(min=8,
                                        message="Your password must have at least 8 characters"), EqualTo('confirm_password', message='Passwords must match')
                             ])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Reset Password')

            


