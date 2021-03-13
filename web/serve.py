from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, UserMixin, current_user, login_required, logout_user
from datetime import datetime
import os
from .forms import LoginForm
from dotenv import load_dotenv
from .models import db, User
from flask import current_app as app

db = SQLAlchemy(app)

load_dotenv()
login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    return render_template('index.html', form=form)

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Logging in")
    if current_user.is_authenticated:
        print("Authenticated")
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main'))
    return render_template('index.html', form=form)

@app.route('/main')
def main():
    return render_template('main.html')

if __name__ == '__main__':
    app.run()