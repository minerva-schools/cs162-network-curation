import requests

# Example taken from:
# http://flask.pocoo.org/docs/1.0/testing/
# and suitably modified.
import os
import tempfile

import pytest

from web import create_app, db
from web.models import Users, UserConnections
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

def add_connection(client, name, contact_by, last_contacted):
    return client.post(
        "/add_connection",
        data=dict(name=name, contact_by=contact_by, last_contacted=last_contacted),
        follow_redirects=True,
    )

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

'''
def test_basic_request():
    r = requests.get("http://127.0.0.1:5000/")
    assert r.status_code == 200
'''
from web.serve import get_overdue 
from datetime import date, timedelta

def test_login(client):
    db.drop_all()
    db.create_all()

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

    assert UserConnections.query.filter_by(name="ConnectionAddedIntegration").first() is None
    assert UserConnections.query.filter_by(name="NotOverdueIntegration").first() is None
    rv = add_connection(client, "ConnectionAddedIntegration", date.today(), date.today() - timedelta(days=1))
    assert rv.status_code == 200
    rv = add_connection(client, "NotOverdueIntegration", date.today() - timedelta(days=1), date.today())
    assert UserConnections.query.filter_by(name="ConnectionAddedIntegration").first() is not None
    assert UserConnections.query.filter_by(name="NotOverdueIntegration").first() is not None
    rv = client.get('/', follow_redirects=True)
    assert rv.status_code == 200

    connections = UserConnections.query.all()
    overdue_connections = get_overdue(connections)
    overdue_names = [connection.name for connection in overdue_connections]
    assert "ConnectionAddedIntegration" in overdue_names
    assert "NotOverdueIntegration" not in overdue_names

    rv = logout(client)
    assert b"Add a Connection" not in rv.data