from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, UserMixin, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from forms import LoginForm
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

db.create_all()
example_user = User(id=1, name="Philip Sterne", username="username", password="password")
db.session.merge(example_user)
db.session.commit()

@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html', form=form)

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('index.html', title='Sign In', form=form)


if __name__ == '__main__':
    app.run()
