# Example taken from:
# http://flask.pocoo.org/docs/1.0/testing/
# and suitably modified.
import os
import tempfile

import pytest

from web import create_app, db
from web.models import Users

app = create_app()


def signup(client, username, email, passwd, confirm_passwd):
    return client.post(
        "/signup",
        data=dict(
            user_name=username,
            email=email,
            password=passwd,
            confirm_password=confirm_passwd,
        ),
        follow_redirects=True,
    )


def login(client, email_or_username, password):
    return client.post(
        "/login",
        data=dict(email_or_username=email_or_username, password=password),
        follow_redirects=True,
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)


@pytest.fixture
def client():

    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    # User used for test
    app.config["USERNAME"] = "somethingsomething"
    app.config["EMAIL"] = "phillip@sterne.com"
    app.config["PASSWORD"] = "Poodles01$"

    app.app_context().push()

    with app.app_context():
        db.create_all()
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config["DATABASE"])


def test_incorrect_signup(client):

    # too short of a password
    rv = signup(client, app.config["USERNAME"], app.config["EMAIL"], "s", "s")
    assert Users.query.filter_by(name=app.config["USERNAME"]).first() is None
    assert b"Field must be at least 8 characters long" in rv.data

    # passwords don't match
    rv = signup(
        client, app.config["USERNAME"], app.config["EMAIL"], "Poodles1", "OzzyDogs1"
    )
    assert Users.query.filter_by(name=app.config["USERNAME"]).first() is None
    assert b"Passwords must match" in rv.data

    # invalid email address
    rv = signup(
        client,
        app.config["USERNAME"],
        "lol",
        app.config["PASSWORD"],
        app.config["PASSWORD"],
    )
    assert Users.query.filter_by(name=app.config["USERNAME"]).first() is None
    assert b"Enter a valid email" in rv.data

    # too short of a username
    rv = signup(
        client,
        "nope",
        app.config["EMAIL"],
        app.config["PASSWORD"],
        app.config["PASSWORD"],
    )
    assert Users.query.filter_by(name="nope").first() is None
    assert b"Username must be between 5 &amp; 25 characters" in rv.data

    # username has a dollar sign
    rv = signup(
        client,
        app.config["USERNAME"] + "$",
        app.config["EMAIL"],
        app.config["PASSWORD"],
        app.config["PASSWORD"],
    )
    assert Users.query.filter_by(name=app.config["USERNAME"] + "$").first() is None
    assert b"Username must contain only letters, numbers or underscore" in rv.data

def test_correct_signup(client):
    # valid signup
    rv = signup(
        client,
        app.config["USERNAME"],
        app.config["EMAIL"],
        app.config["PASSWORD"],
        app.config["PASSWORD"],
    )
    assert Users.query.filter_by(name=app.config["USERNAME"]).first() is not None


def test_correct_login(client):
    # LOGIN VIA USERNAME
    rv = login(client, app.config["USERNAME"], app.config["PASSWORD"])
    assert b"Add a Connection" in rv.data
    assert b"Login" not in rv.data

    rv = logout(client)
    assert b"Add a Connection" not in rv.data

    # LOGIN VIA EMAIL
    rv = login(client, app.config["EMAIL"], app.config["PASSWORD"])
    assert b"Add a Connection" in rv.data
    assert b"Login" not in rv.data

    rv = logout(client)
    assert b"Add a Connection" not in rv.data

    assert Users.query.filter_by(name=app.config["USERNAME"]).first() is not None


def test_invalid_login_credentials(client):
    # invalid username
    rv = login(client, app.config["USERNAME"] + "x", app.config["PASSWORD"])
    assert b"Invalid email or username" in rv.data

    # invalid password
    rv = login(client, app.config["USERNAME"], app.config["PASSWORD"] + "x")
    assert b"Invalid password" in rv.data
    assert Users.query.filter_by(name=app.config["USERNAME"]).first() is not None
