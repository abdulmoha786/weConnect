# from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# from app import login
from flask_bcrypt import Bcrypt


# @login.user_loader
# def load_user(id):
#     pass


# return User.query.get(int(id))


class User (object):
    users = []

    def __init__(self):
        self.user_id = ""
        self.username = ""
        self.email = ""
        self.password_hash = ""
        self.login = False

    def __init__(self, user_id, username, email, password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.login = False

    def set_password(self, password):
        pass

    def create_user(self, user_id, username, email, password):
        self.username = username
        self.email = email
        self.user_id = user_id
        self.password_hash = generate_password_hash (password)

        user = {'user_id': user_id,
                'username': username,
                'email': email,
                'password_hash': self.password_hash
                }

        if user in User.users:
            message = {'user': user['username'],
                       'message': "User Exists"}
            return message
        else:
            User.users.append (user)
            message = {'user': user['username'],
                       'message': "User created successfully"}
            return message

    def check_password(self, password):
        return check_password_hash (self.password_hash, password)

    def __repr__(self):
        return {'user_id': self.user_id,
                'username': self.username,
                'email': self.email,
                'password_hash': self.password_hash
                }


class Business (object):
    businesses = []

    def __init__(self, business_id, owner, name, profile):
        self.id = business_id
        self.name = name
        self.owner = owner
        self.profile = profile
        self.reviews = []

    @staticmethod
    def delete_business(business_id):
        for business in Business.businesses:
            if business.id == business_id:
                Business.businesses.remove (business)

    def review_business(self):
        pass


class Review (object):
    reviews = []

    def __init__(self, review_id, business_id, review_text):
        self.review_id = review_id
        self.review_text = review_text
        self.business_id = business_id

    def delete_review(self):
        pass

    def get_review(self, review_id):
        pass
