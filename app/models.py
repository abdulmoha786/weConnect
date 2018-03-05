from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from app import db
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User (UserMixin, username, email, password_hash):
    self.username = username
    self.email = email
    self.password_hash = password_hash
    businesses = []

    def __repr__(self):
        return '<user {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)