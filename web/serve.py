from flask import current_app as app, session
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user

from . import db, login
from .forms import LoginForm, SignupForm, AddConnectionForm
from .models import User, UserConnection


@login.user_loader
def load_user(user_id):
    """Finds the user given their id"""
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user is not None and current_user.is_authenticated:
        print("Authenticated")
        return redirect(url_for('main'))
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # TODO: switch to a logging framework
    print("Signing up")

    if current_user is not None and current_user.is_authenticated:
        print("Authenticated")
        return redirect(url_for('main'))

    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data).first() or User.query.filter_by(
                username=form.email.data).first()
        if user is None:
            # Create a new user
            user = User(username=form.username.data, name=form.name.data, email=form.email.data, phone=form.phone.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main'))
        else:
            flash('That username is taken. Please choose another.')
    return render_template('signup.html', form=form)


@app.route('/addconnection', methods=['GET', 'POST'])
@login_required
def addconnection():
    print("Adding Connection")
    form = AddConnectionForm()
    connection = UserConnection(userid=current_user.id,
                        name=form.name.data,
                        title=form.title.data,
                        email=form.email.data,
                        phone=form.phone.data)
    db.session.add(connection)
    db.session.commit()
    return redirect(url_for('main'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # TODO: switch to a logging framework
    print("Logging in")
    if current_user is not None and current_user.is_authenticated:
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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    # Clear the flash stream
    session.pop('_flashes', None)
    return redirect(url_for("index"))


@app.route('/main')
@login_required
def main():
    print(current_user.id)
    connections = UserConnection.query.filter_by(userid=current_user.id).all()
    form = AddConnectionForm()
    return render_template('index.html', connections=connections, form=form)


if __name__ == '__main__':
    app.run()
