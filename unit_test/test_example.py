# Example taken from:
# http://flask.pocoo.org/docs/1.0/testing/
# and suitably modified.
import os
import tempfile

import pytest

from web import create_app

app = create_app()


def signup(client, username, email, password):
    return client.post('/signup', data=dict(
        username=username,
        email=email,
        password=password
    ), follow_redirects=True)


def login(client, email_or_username, password):
    return client.post('/login', data=dict(
        email_or_username=email_or_username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    # User used for test
    app.config['USERNAME'] = 'philip'
    app.config['EMAIL'] = 'sterne@rome.empire'
    app.config['PASSWORD'] = 'myPassword'

    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_signup_login_logout(client):
    """Make sure login and logout works."""

    # TODO: ADD Assertion statements to carry out the test

    rv = signup(client, app.config['USERNAME'], app.config['EMAIL'], app.config['PASSWORD'])
    # assert b'You were logged in' in rv.data

    rv = logout(client)
    # assert b'You were logged out' in rv.data

    # LOGIN VIA USERNAME
    rv = login(client, app.config['USERNAME'], app.config['PASSWORD'])
    # assert b'You were logged in' in rv.data

    rv = logout(client)
    # assert b'You were logged out' in rv.data

    # LOGIN VIA EMAIL
    rv = login(client, app.config['EMAIL'], app.config['PASSWORD'])
    # assert b'You were logged in' in rv.data

    rv = logout(client)

    rv = login(client, app.config['USERNAME'] + 'x', app.config['PASSWORD'])
    # assert b'Invalid username' in rv.data

    rv = login(client, app.config['USERNAME'], app.config['PASSWORD'] + 'x')
    # assert b'Invalid password' in rv.data
