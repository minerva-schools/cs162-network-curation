from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, UserMixin, current_user, login_required, logout_user
from datetime import datetime
import os
from .forms import LoginForm, SignupForm
from flask import current_app as app
from . import db, login
from .models import User


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print("Signing up")

    if current_user.is_authenticated:
        print("Authenticated")
        return redirect(url_for('main'))

    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, )
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main'))
    return render_template('signup.html', form=form)


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
    return render_template('login.html', form=form)


@app.route('/main')
@login_required
def main():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
