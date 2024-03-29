import os
import sys

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)
from web.models import Users, UserConnections
from web import create_app, db
from web.serve import get_overdue
import unittest
from datetime import date, timedelta


class UserModelTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_adding(self):
        user = Users()
        self.assertTrue(user is not None)

    def test_pw_set(self):
        user = Users()
        user.set_password("pwd123")
        self.assertTrue(user.password_hash is not None)

    def test_pwd_verification(self):
        user = Users()
        user.set_password("pwd123")
        self.assertTrue(user.check_password("pwd123"))
        self.assertFalse(user.check_password("pd13"))

    def test_pwd_salts_are_random(self):
        user = Users()
        user.set_password("pwd123")
        user2 = Users()
        user2.set_password("pwd123")
        self.assertTrue(user.password_hash != user2.password_hash)


class UserConnectionModelTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_userconnection_adding(self):
        userconnection = UserConnections(
            id=1,
            contact_by=date.today(),
            last_contacted=date.today() - timedelta(days=1),
        )
        self.assertTrue(userconnection is not None)


if __name__ == "__main__":
    unittest.main()