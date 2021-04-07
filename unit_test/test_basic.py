import unittest
from flask import current_app
import os
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)
from web import create_app, db

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_existence(self):
        self.assertTrue(current_app is not None)

    def test_app_testing(self):
        self.assertTrue(current_app.config['TESTING'])

if __name__ == "__main__":
    unittest.main()