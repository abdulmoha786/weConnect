import unittest
from flask import current_app, jsonify
import json
from app import app
from app.models import User, Business, Review
from config import TestingConfig


class WeconnectTestCase (unittest.TestCase):
    """This class represents the weconnect Testcase"""

    def setUp(self):
        """Define variables and initialize app."""
        # testapp = app
        # app.config.from_object(TestingConfig)
        self.client = app.test_client ()
        self.client.testing = True
        # self.user_id = 1
        # self.username = "Abdulaziz"
        # self.email = "myemail.com"
        # self.password = "mypassword"
        self.user = User (1, "Abdulaziz", "myemail.com", "mypassword")
        # self.business = Business()

    def test_app_creation(self):
        """"""
        pass

    def test_create_user(self):
        """"""
        user_data = {'user_id': self.user.user_id,
                     'username': self.user.username,
                     'email': self.user.email,
                     'password': self.user.password_hash}

        res = self.client.post('/api/v1/auth/register', data=json.dumps(user_data),
                               headers={'content-type': 'application/json'})
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.user.username, str(res.data))

    def test_login(self):
        """"""
        login_data = {
                      'username': "Abdulaziz",
                      'password': "mypassword"
                     }
        res = self.client.post('/api/v1/auth/login', data=json.dumps(login_data),
                               headers={'content-type': 'application/json'})
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.user.username, str(res.data))

    def test_logout(self):
        """"""
        data = {
                'email':"myemail.com"
               }
        res = self.client.post('/api/v1/auth/logout', data=json.dumps(data),
                               headers={'content-type': 'application/json'})
        self.assertEqual(res.status_code, 200)

    def test_reset_password(self):
        """"""
        pass

    def test_register_business(self):
        """"""
        pass

    def test_update_business_profile(self):
        """"""
        pass

    def test_delete_business(self):
        """"""
        pass

    def test_retrieve_business(self):
        """"""
        pass

    def test_get_a_business(self):
        """"""
        pass

    def test_add_review(self):
        """"""
        pass

    def test_get_reviews(self):
        """"""
        pass


if __name__ == "__main__":
    unittest.main()
