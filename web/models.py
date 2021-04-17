"""
Define object models for the application

Current models:
    - Users:
        - Attributes:
            - ID
            - Name
            - Username
            - Password hash
        - Methods:
            - Set password
            - Check password

"""
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from datetime import datetime

from . import db


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), unique=True)
    password_hash = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    date_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    email_confirmed = db.Column(db.Boolean(), nullable=False, default=False)
    email_confirm_date = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    def get_mail_confirm_token(self, expires_sec=1800):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.email}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        try:
            s = Serializer(app.config["SECRET_KEY"])
            user_id = s.loads(token)["user_id"]
            return Users.query.get(user_id)
        except (SignatureExpired, BadSignature):
            return None

    def verify_mail_confirm_token(token):
        try:
            s = Serializer(app.config["SECRET_KEY"])
            email = s.loads(token)
            return email
        except (SignatureExpired, BadSignature):
            return None


class UserConnections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String(200))
    title = db.Column(db.String(600))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(50))
    tags = db.Column(db.String(200))
    contact_by = db.Column(db.Date())
    last_contacted = db.Column(db.Date())
    note = db.Column(db.String(2000))
    users = db.relationship("Users", foreign_keys=userid)
