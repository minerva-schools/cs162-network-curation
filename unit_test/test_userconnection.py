# Example taken from:
# http://flask.pocoo.org/docs/1.0/testing/
# and suitably modified.
import os
import tempfile

import pytest

from web import create_app, db
from web.models import UserConnections
from web.serve import get_overdue
from datetime import date, timedelta 

app = create_app()


@pytest.fixture
def client():

    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    app.app_context().push()

    with app.app_context():
        db.create_all()
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config["DATABASE"])

def test_userconnection_add(client):
    test_user = UserConnections(
        id=1,
        contact_by=date.today(),
        last_contacted=date.today() - timedelta(days=1),
    )
    db.session.add(test_user)
    db.session.commit()
    assert UserConnections.query.filter_by(id=1).first() is not None

def test_overdue_checker(client):
    db.drop_all()
    db.create_all()
    test_user = UserConnections(
        id=1,
        contact_by=date.today(),
        last_contacted=date.today() - timedelta(days=1),
    )
    db.session.add(test_user)
    db.session.commit()
    connections = UserConnections.query.all()
    overdue_connections = get_overdue(connections)
    assert overdue_connections[0].id is 1

    

