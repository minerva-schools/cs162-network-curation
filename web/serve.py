from flask import current_app as app, session
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, login_required, logout_user

from .models import Users, UserConnections, db
from . import login, mail
from .forms import (
    LoginForm,
    SignupForm,
    AddConnectionForm,
    RequestResetForm,
    ResetPasswordForm,
)
from flask_mail import Message

from datetime import datetime, date


@login.user_loader
def load_user(user_id):
    """Finds the user given their id"""
    return Users.query.get(int(user_id))


@app.route("/", methods=["GET", "POST"])
def index():
    if current_user is not None and current_user.is_authenticated:
        print("Authenticated")
        return redirect(url_for("main"))
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    # TODO: switch to a logging framework
    print("Signing up")

    if current_user is not None and current_user.is_authenticated:
        print("Authenticated")
        return redirect(url_for("main"))

    form = SignupForm()
    if form.validate_on_submit():
        user_name = Users.query.filter_by(name=form.user_name.data).first()
        user_email = Users.query.filter_by(email=form.email.data).first()
        if user_email:
            flash("That email is taken. Please choose another one.")
        elif user_name:
            flash("That username is taken. Please choose another one.")
        else:
            # Create a new user
            user = Users(name=form.user_name.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("main"))

    return render_template("signup.html", form=form)


@app.route("/add_connection", methods=["GET", "POST"])
@login_required
def add_connection():
    print("Adding Connection")
    form = AddConnectionForm()
    # Prevent raising errors when optional fields are not filled
    filled_next_reminder = None
    try:
        filled_next_reminder = datetime.strptime(form.next_reminder.data, "%Y-%m-%d").date()
    except ValueError:
        pass
    filled_last_contacted = None
    try:
        filled_last_contacted = datetime.strptime(
            form.last_contacted.data, "%Y-%m-%d"
        ).date()
    except ValueError:
        pass

    connection = UserConnections(
        userid=current_user.id,
        name=form.name.data,
        title=form.title.data,
        email=form.email.data,
        phone=form.phone.data,
        next_reminder=filled_next_reminder,
        last_contacted=filled_last_contacted,
        tags=form.tags.data,
        note=form.note.data,
    )
    db.session.add(connection)
    db.session.commit()
    return redirect(url_for("main"))


@app.route("/login", methods=["GET", "POST"])
def login():
    # TODO: switch to a logging framework
    print("Logging in")
    if current_user is not None and current_user.is_authenticated:
        print("Authenticated")
        return redirect(url_for("main"))
    form = LoginForm()
    if form.validate_on_submit():
        user_name = Users.query.filter_by(name=form.email_or_username.data).first()
        user_email = Users.query.filter_by(email=form.email_or_username.data).first()
        user = user_name or user_email
        if user is None:
            flash("Invalid email or username.")
            return redirect(url_for("index"))
        elif not user.check_password(form.password.data):
            flash("Invalid password")
            return redirect(url_for("index"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("main"))
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    # Clear the flash stream
    session.pop("_flashes", None)
    return redirect(url_for("index"))


@app.route("/main")
@login_required
def main():
    print("user:", current_user.id)
    connections = UserConnections.query.filter_by(userid=current_user.id).all()
    form = AddConnectionForm()
    overdue_connections = get_overdue(connections)
    badge_num = len(overdue_connections)
    return render_template(
        "index.html",
        connections=connections,
        overdue_connections=overdue_connections,
        badge_num=badge_num,
        form=form,
    )


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Password Reset Request",
        sender="projectplink@gmail.com",
        recipients=[user.email],
    )

    msg.body = f"""To reset your password, visit the following link \
    {url_for('reset_token', token=token, _external=True)} \
    If you did not make this request then simply ignore this email."""
    mail.send(msg)


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for("main"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user_name = Users.query.filter_by(name=form.email_or_username.data).first()
        user_email = Users.query.filter_by(email=form.email_or_username.data).first()
        user = user_name or user_email
        if user is None:
            flash(
                "Invalid email or username. If you don't have an account yet, you must sign up first."
            )
            return redirect(request.url)
        send_reset_email(user)
        flash(
            "An email has been sent with instructions to reset your password.", "info"
        )
        return redirect(url_for("login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for("main"))
    user = Users.verify_reset_token(token)
    if user is None:
        flash("That is an invalid/expired token", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been updated!")
        return redirect(url_for("login"))
    return render_template("reset_token.html", title="Reset Password", form=form)


def get_overdue(connections):
    overdue_connections = []
    for connection in connections:
        if connection.next_reminder and connection.next_reminder <= date.today():
            if (
                not connection.last_contacted
                or connection.last_contacted < connection.next_reminder
            ):
                overdue_connections.append(connection)
    return overdue_connections


@app.route("/contact/<contactid>")
@login_required
def contact(contactid):
    connection = (
        UserConnections.query.filter_by(userid=current_user.id)
        .filter_by(id=contactid)
        .first()
    )
    print(connection)
    if connection:
        connection.last_contacted = date.today()
        db.session.commit()
    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run()
