from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
login_manager = LoginManager()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)


db.create_all()
example_user = User(id=1, name="Philip Sterne", username="username", password="password")
db.session.merge(example_user)
db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run()
