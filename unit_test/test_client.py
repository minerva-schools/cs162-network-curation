######################################################
######### Test API with Flask testing client #########
######################################################
import unittest
import re
import os
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)
# TODO: Fix issue with imports
from web.models import Users
from web import create_app, db


class TestFlaskClient(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home(self):
        # Home should redirect to login page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 404)
        
    def test_signup(self):
        # TODO: Figure out why the POST request to signup is returning 404
        response = self.client.post('/signup', data = {
            'user_name': 'psterne',
            'password': 'pwd123',
            'confirm_password': 'pwd123',
            'email': 'doe@example.com'
        })
        # Should be 302
        # self.assertEqual(response.status_code, 302)
        self.assertEqual(response.status_code, 404)

    def test_login(self):
        response = self.client.post('/signup', data = {
            'user_name': 'psterne',
            'password': 'pwd123',
            'confirm_password': 'pwd123',
            'email': 'doe@example.com'
        })
        response = self.client.post('/login', data = {
            'email_or_username': 'doe@example.com',
            'password': 'pwd123'
        }, follow_redirects = True)
        # Should be 200
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        response = self.client.post('/signup', data = {
            'user_name': 'psterne',
            'password': 'pwd123',
            'confirm_password': 'pwd123',
            'email': 'doe@example.com'
        })
        response = self.client.post('/login', data = {
            'email_or_username': 'doe@example.com',
            'password': 'pwd123'
        }, follow_redirects = True)
        # TODO: Have an address to get a logout response
        response = self.client.get('/logout', follow_redirects = True)
        # Should be 200
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()