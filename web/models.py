"""
Define object models for the application

Current models:
    - User:
        - Attributes:
            - ID
            - Name
            - Username
            - Password hash
        - Methods:
            - Set password
            - Check password

"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), unique=True)
    password_hash = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserConnection(db.Model):
    __tablename__ = 'userconnections'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(200))
    title = db.Column(db.String(600))
    email = db.Column(db.String(128), unique=True)
    phone = db.Column(db.Integer)
    tag = db.Column(db.String(200))
    contactby = db.Column(db.String(200))
    lastcontacted = db.Column(db.String(200))
    note = db.Column(db.String(2000))
    users = db.relationship('User', foreign_keys=userid)