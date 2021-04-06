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

from . import db


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), unique=True)
    password_hash = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']

        # TODO: use a narrower exception
        except Exception:
            return None
        return Users.query.get(user_id)


class UserConnections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(200))
    title = db.Column(db.String(600))
    email = db.Column(db.String(128))
    phone = db.Column(db.Integer)
    tags = db.Column(db.String(200))
    contact_by = db.Column(db.Date())
    last_contacted = db.Column(db.Date())
    note = db.Column(db.String(2000))
    users = db.relationship('Users', foreign_keys=userid)
