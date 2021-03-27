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
    __tablename__ = 'users'
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

class Note(UserMixin, db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(600))
    locationmet = db.Column(db.String(200))
    label = db.Column(db.String(10))


class UserNotes(UserMixin, db.Model):
    __tablename__ = 'usernotes'
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    noteid = db.Column(db.Integer, db.ForeignKey('notes.id'), primary_key=True)
    users = db.relationship('User', foreign_keys=userid)
    notes = db.relationship('Note', foreign_keys=noteid)