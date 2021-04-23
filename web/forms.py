from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    BooleanField,
    PasswordField,
    TextAreaField,
    HiddenField,
)
from wtforms.fields.html5 import EmailField, TelField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp


class LoginForm(FlaskForm):
    email_or_username = StringField(
        "Email Address or Username", validators=[DataRequired()]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class SignupForm(FlaskForm):
    user_name = StringField(
        "Username",
        validators=[
            DataRequired(),
            Regexp(
                r"^\w+$",
                message="Username must contain only letters, numbers or underscore",
            ),
            Length(min=5, max=25, message="Username must be between 5 & 25 characters"),
        ],
    )
    password = PasswordField(
        "Password (8 characters+)",
        validators=[
            DataRequired(),
            Length(min=8, message="Your password must have at least 8 characters"),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    email = StringField(
        "Email Address", validators=[DataRequired(), Email("Enter a valid email")]
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign Up")


class AddConnectionForm(FlaskForm):
    name = StringField("Connection Name", validators=[DataRequired()])
    phone = TelField("Phone")
    email = EmailField("Email Address", validators=[Email("Enter a valid email")])
    tags = HiddenField("Tags")
    next_reminder = StringField(
        "Next Reminder Date",
    )
    last_contacted = StringField(
        "Last Contacted",
    )
    note = TextAreaField("Note")
    submit = SubmitField("Add Connection")


class RequestResetForm(FlaskForm):
    email_or_username = StringField(
        "Email Address or Username", validators=[DataRequired()]
    )
    submit = SubmitField("Request Password Reset")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Your password must have at least 8 characters"),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo("confirm_password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Reset Password")