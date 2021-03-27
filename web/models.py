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

from .serve import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    username = db.Column(db.String(200), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    phone = db.Column(db.Integer)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserConnection(UserMixin, db.Model):
    id1 = db.Column(db.Integer, primary_key=True)
    id2 = db.Column(db.Integer)
