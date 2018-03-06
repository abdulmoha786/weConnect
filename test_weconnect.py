import unittest
import json
from app import app
from app.models import User,Business,Review

class WeconnectTestCase(unittest.TestCase):
    """This class represents the weconnect Testcase"""


    def setUp(self):
        """Define variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.weconnect = {'name':'weconnect app'}

    def test_app_creation(self):
        """"""
        pass

    def test_create_user(self):
        """"""
        pass

    def test_login(self):
        """"""
        pass

    def test_login(self):
        """"""
        pass

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
    