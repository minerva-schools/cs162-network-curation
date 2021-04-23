import requests

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
    app.config["USERNAME"] = "sotdsasad"
    app.config["EMAIL"] = "phillip@sterne.com"
    app.config["PASSWORD"] = "Poodleds01$"

    app.app_context().push()

    with app.app_context():
        db.create_all()
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config["DATABASE"])

def test_basic_request():
    r = requests.get("http://127.0.0.1:5000/")
    assert r.status_code == 200

def test_login(client):
    # valid signup
    rv = signup(
        client,
        app.config["USERNAME"],
        app.config["EMAIL"],
        app.config["PASSWORD"],
        app.config["PASSWORD"],
    )
    assert Users.query.filter_by(name=app.config["USERNAME"]).first() is not None

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