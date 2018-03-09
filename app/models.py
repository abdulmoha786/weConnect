from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class User (object):
    user_list = []

    def __init__(self, user_id, username, email, password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.login = False

    def generate_auth_token(self, expiration=600):
        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'email': self.email})

    def reset_password(self, new_password):
        new_password_hash = generate_password_hash(new_password)
        self.password_hash = new_password_hash

    @staticmethod
    def verify_auth_token(token, users):
        s = Serializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.get_user_by_email(data['email'], users)
        return user

    def __eq__(self, other):
        return self.email == other.email

    @staticmethod
    def get_user(user_id):
        for user in User.user_list:
            if user.user_id == user_id:
                return user
        return None

    @staticmethod
    def get_user_by_email(email, users):
        for user in users:
            if user.email == email:
                return user
        return None

    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        if self.__index >= len(User.user_list) - 1:
            raise StopIteration
        self.__index += 1
        user = User.user_list[self.__index]
        return user

    def __repr__(self):
        return {'user_id':self.user_id,
                'username': self.username,
                'email':self.email
                }

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Business (object):
    businesses = []

    def __init__(self, business_id, owner, name, location, profile):
        self.id = business_id
        self.name = name
        self.location = location
        self.owner = owner
        self.profile = profile
        self.reviews = []

    @staticmethod
    def delete_business(business_id):
        for business in Business.businesses:
            if business.id == business_id:
                Business.businesses.remove(business)

    @staticmethod
    def get_business(business_id):
        for business in Business.businesses:
            if business.id == business_id:
                return business
        return None

    def review_business(self, review):
        self.reviews.append(review)

    def delete_review(self, review_id, owner):
        review = Review.get_review(review_id, self.reviews)
        if review is not None and review.user_id == owner:
            self.reviews.remove(review)

    def __eq__(self, other):
        return self.id == other.id

    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        if self.__index >= len(Business.businesses) - 1:
            raise StopIteration
        self.__index += 1
        business = Business.businesses[self.__index]
        return business

    def __repr__(self):
        return {'id':self.id,
                'name':self.name,
                'location':self.location,
                'owner':self.owner,
                'profile':self.profile
                }


class Review (object):
    reviews = []

    def __init__(self, review_id, business_id,  user_id, review_text):
        self.review_id = review_id
        self.review_text = review_text
        self.business_id = business_id
        self.user_id = user_id

    def delete_review(self):
        pass

    @staticmethod
    def get_review(review_id, reviews):
        for review in reviews:
            if review.review_id == review_id:
                return review
        return None

    def update_review(self, review_text):
        self.review_text = review_text

    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        if self.__index >= len(Review.reviews) - 1:
            raise StopIteration
        self.__index += 1
        review = Review.reviews[self.__index]
        return review

    def __repr__(self):
        return {'review_id':self.review_id,
                'review_text':self.review_text,
                'business_id':self.business_id,
                'user_id':self.user_id
                }