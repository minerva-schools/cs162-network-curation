# Example taken from:
# http://flask.pocoo.org/docs/1.0/testing/
# and suitably modified.
import os
import tempfile

import pytest

from web import create_app, db
from web.models import Users

app = create_app()


def signup(client, username, email, passwd):
    print(passwd)
    return client.post(
        "/signup",
        data=dict(user_name=username, email=email, password=passwd, confirm_password=passwd),
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
    app.config["USERNAME"] = "parkercline"
    app.config["EMAIL"] = "parker@parker.com"
    app.config["PASSWORD"] = "Poodles01$"

    app.app_context().push()

    with app.app_context():
        db.create_all()
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config["DATABASE"])


def test_signup_login_logout(client):
    """Make sure login and logout works."""

    # TODO: ADD Assertion statements to carry out the test

    rv = signup(
        client, app.config["USERNAME"], app.config["EMAIL"], app.config["PASSWORD"]
    )
    assert Users.query.filter_by(name=app.config["USERNAME"]).first() is not None

    # LOGIN VIA USERNAME
    rv = login(client, app.config["USERNAME"], app.config["PASSWORD"])
    assert b"Add a Connection" in rv.data
    assert b"Login" not in rv.data

    rv = logout(client)
    assert b'Add a Connection' not in rv.data

    # LOGIN VIA EMAIL
    rv = login(client, app.config["EMAIL"], app.config["PASSWORD"])
    assert b"Add a Connection" in rv.data
    assert b"Login" not in rv.data

    rv = logout(client)
    assert b'Add a Connection' not in rv.data

    rv = login(client, app.config["USERNAME"] + "x", app.config["PASSWORD"])
    assert b'Invalid email or username' in rv.data

    rv = login(client, app.config["USERNAME"], app.config["PASSWORD"] + "x")
    assert b'Invalid password' in rv.data
    assert Users.query.filter_by(name=app.config["USERNAME"]).first() is not None
