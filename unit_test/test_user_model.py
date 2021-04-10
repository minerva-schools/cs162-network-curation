import os
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)
from web.models import User, UserConnection
from web import create_app, db
from werkzeug.security import generate_password_hash, check_password_hash
import unittest

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

    def test_pw_set(self):
        user = User()
        user.set_password('pwd123')
        self.assertTrue(user.password_hash is not None)

    def test_pwd_verification(self):
        user = User()
        user.set_password('pwd123')
        self.assertTrue(user.check_password('pwd123'))
        self.assertFalse(user.check_password('pd13'))

    def test_pwd_salts_are_random(self):
        user = User()
        user.set_password('pwd123')
        user2 = User()
        user2.set_password('pwd123')
        self.assertTrue(user.password_hash != user2.password_hash)

if __name__ == "__main__":
    unittest.main()