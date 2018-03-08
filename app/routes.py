from flask import request, jsonify, Blueprint, g
from app.models import User, Business, Review
from flask_httpauth import HTTPBasicAuth

# from app import app


bp = Blueprint ('app', __name__, url_prefix='/api/v1/')
auth = HTTPBasicAuth()
users = []
business = []
review = []

@bp.route('auth/')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token, users)
    if not user:
        user = User.get_user_by_email(username_or_token, users)
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True


@bp.route ('auth/register', methods=['POST'])
def create_user():
    data = request.get_json ()
    username = data['username']
    email = data['email']
    password = data['password']
    user_id = data['user_id']
    user = User(user_id, username, email, password)
    if user in users:
        message = {'username': user.username,
                   'status': 'User Exists'}
        return jsonify(message)
    else:
        users.append(user)
        message = {'username': user.username,
                   'status': 'User created successfully'
                   }
        return jsonify(message)


@bp.route('auth/login', methods=['POST'])
def login():
    data = request.get_json()
    # if verify_password(data['username'],data['password']):
    #     pass
    for user in users:
        if user.username == data['username'] and user.check_password(data['password']):
            user.login = True
            message = {
                         'user': data['username'],
                         'message': "Login Successful"
                      }
            return jsonify(message)
    message = {
                'user': data['username'],
                'message': "Login Unsuccessful"
              }
    return jsonify(message)


@bp.route('auth/logout', methods=['POST'])
def logout():
    data = request.get_json()
    for user in users:
        if user.email == data['email']:
            user.login = False
            message = {
                        'username': user.username,
                        'message':'User Logged out'
                      }
            return jsonify(message)
    message = {
                'username':'User Not Logged in'
              }
    return jsonify (message)


@bp.route('/api/auth/reset-password', methods=['POST'])
def reset_password(old_password, new_password):
    pass


@bp.route ('/api/businesses', methods=['POST'])
def register_business():
    data = request.get_json()



@bp.route ('/api/businesses/<businessId>', methods=['PUT'])
def update_business_profile():
    pass


@bp.route ('/api/businesses/<businessId>', methods=['DELETE'])
def delete_business():
    pass


@bp.route ('/api/businesses', methods=['GET'])
def retrieve_businesses(old_password, new_password):
    pass


@bp.route ('/api/businesses/<businessId>', methods=['GET'])
def get_a_business():
    pass


@bp.route ('/api/businesses/<businessId>/reviews', methods=['POST'])
def add_review():
    pass


@bp.route ('/api/businesses/<businessId>/reviews', methods=['GET'])
def get_reviews():
    pass
