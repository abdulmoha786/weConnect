# from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# from app import login
# from flask_bcrypt import Bcrypt


# @login.user_loader
# def load_user(id):
#     pass


# return User.query.get(int(id))

class User (object):
    users = []

    def __init__(self, user_id, username, email, password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.login = False

    def __eq__(self, other):
        return self.email == other.email

    def set_password(self, password):
        pass

    @staticmethod
    def add_user(user):
        User.users.append (user)

    # def __iter__(self):
    #     self.__index = -1
    #     return self
    #
    # def __next__(self):
    #     if self.__index >= len(users)-1:
    #         raise StopIteration
    #     self.__index += 1
    #     user = User.users[self.__index]
    #     return user

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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
