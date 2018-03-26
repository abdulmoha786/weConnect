import unittest

import json
from app import app
from app.models import User, Business, Review


class WeconnectTestCase (unittest.TestCase):
    """This class represents the weconnect Testcase"""

    def setUp(self):
        """Define variables and initialize app."""
        self.client = app.test_client ()
        self.client.testing = True
        self.user = User (1, "Abdulaziz", "myemail.com", "mypassword")
        self.user2 = User(2, "Rajab", "rajab.com", "hispassword")
        self.business = Business(1,self.user.email, "my business", "Roysambu", "my business is good")
        self.review = Review(1,1,1,"Your business is great")

    def test_user_generates_auth_token(self):
        users = [self.user]
        self.user.__list = users
        token = self.user.generate_auth_token()
        user2 = User.verify_auth_token(token, users)
        self.assertEqual(user2, self.user)

    def test_create_user(self):
        """"""
        user_data = self.user.__repr__()
        user_data['password'] = 'mypassword'
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
        user_data = self.user.__repr__()
        user_data['password'] = "mypassword"
        new_password = "mynewpassword"

        data = {
                'email':self.user.email,
                'new_password':new_password,
                'new_password_confirm':new_password
                }
        res = self.client.post('/api/v1/auth/reset-password', data=json.dumps(data),
                               headers={'content-type': 'application/json'})
        self.assertEqual(res.status_code, 200)

    def test_register_business(self):
        """"""
        #register a non-existent business
        business_data = self.business.__repr__()
        business_data['business_id'] = 3
        res = self.client.post('/api/v1/businesses', data=json.dumps(business_data),
                                headers={'content-type': 'application/json'})
        self.assertEqual(res.status_code, 201)


        #Register an existing business
        res2 = self.client.post ('/api/v1/businesses', data=json.dumps(business_data),
                                headers={'content-type': 'application/json'})
        self.assertEqual(res2.status_code, 500)

    def test_update_business_profile(self):
        """"""
        data = {
                'new_profile':'Here is my business new profile'
                }

        #Response for an existing business
        res = self.client.put('/api/v1/businesses/1', data=json.dumps(data),
                              headers={'content-type': 'application/json'})

        #Response for an inexistent business
        res2 = self.client.put('/api/v1/businesses/2', data=json.dumps(data),
                              headers={'content-type': 'application/json'})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res2.status_code, 300)

    def test_delete_business(self):
        """"""
        #Register a business
        business_data = self.business.__repr__()
        self.client.post('/api/v1/businesses', data=json.dumps (business_data),
                         headers={'content-type': 'application/json'})

        #Delete an existing business
        res = self.client.delete('/api/v1/businesses/' + str(business_data['business_id']),
                               headers={'content-type': 'application/json'})
        self.assertEqual(res.status_code, 200)

        #Delete an inexistent business
        res2 = self.client.delete('/api/v1/businesses/' + str(business_data['business_id'] + 1),
                                  headers={'content-type': 'application/json'})
        self.assertEqual(res2.status_code, 300)

    def test_retrieve_business(self):
        """"""
        #Retrieve businesses from a non-empty list
        res2 = self.client.get('/api/v1/businesses',
                               headers={'content-type': 'application/json'})
        self.assertEqual(res2.status_code, 200)

    def test_get_a_business(self):
        """"""
        # Register a business
        business_data = self.business.__repr__ ()
        self.client.post ('/api/v1/businesses', data=json.dumps(business_data),
                          headers={'content-type': 'application/json'})

        #get the registered business
        res = self.client.get ('/api/v1/businesses/' + str(business_data['business_id']),
                          headers={'content-type': 'application/json'})
        self.assertEqual(res.status_code, 201)

        #Try to get an unregistered business
        res2 = self.client.get ('/api/v1/businesses/' + str(business_data['business_id']+1),
                                headers={'content-type': 'application/json'})
        self.assertEqual(res2.status_code, 400)

    def test_add_review(self):
        """"""
        review_data = self.review.__repr__()

        #Add review to a non-existent business
        res = self.client.post('/api/v1/businesses/' + str(review_data['business_id']+1) + '/reviews',
                               data=json.dumps(review_data),
                               headers = {'content-type': 'application/json'})
        self.assertEqual(res.status_code, 300)

        #register user
        user_data = self.user.__repr__()
        user_data['password'] = 'mypassword'
        self.client.post ('/api/v1/auth/register', data=json.dumps (user_data),
                                headers={'content-type': 'application/json'})

        #Register a business
        business_data = self.business.__repr__ ()
        self.client.post ('/api/v1/businesses', data=json.dumps(business_data),
                          headers={'content-type': 'application/json'})

        #Add review to an existing business
        res2 = self.client.post ('/api/v1/businesses/' + str(review_data['business_id']) + '/reviews',
                                data=json.dumps(review_data),
                                headers={'content-type': 'application/json'})
        self.assertEqual(res2.status_code, 201)
        pass

    def test_get_reviews(self):
        """"""
        res = self.client.get('/api/v1/businesses/' + str(self.business.id) + '/reviews',
                                headers={'content-type': 'application/json'})
        self.assertEqual(res.status_code, 200)

if __name__ == "__main__":
    unittest.main()
