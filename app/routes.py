from flask import request, jsonify, Blueprint, g
from app.models import User, Business, Review
from flask_httpauth import HTTPBasicAuth

# from app import app


bp = Blueprint('app', __name__, url_prefix='/api/v1/')
auth = HTTPBasicAuth()
users = []
businesses = []
review = []

@bp.route('auth/')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token, User.user_list)
    if not user:
        user = User.get_user_by_email(username_or_token, User.user_list)
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True


@bp.route('auth/register', methods=['POST'])
def create_user():
    data = request.get_json ()
    username = data['username']
    email = data['email']
    password = data['password']
    user_id = data['user_id']
    user = User(user_id, username, email, password)
    if user in User.user_list:
        message = {'username': user.username,
                   'status': 'User Exists'}
        return jsonify(message)
    else:
        User.user_list.append(user)
        message = {'username': user.username,
                   'status': 'User created successfully'
                   }
        return jsonify(message)


@bp.route('auth/login', methods=['POST'])
def login():
    data = request.get_json()
    # if verify_password(data['username'],data['password']):
    #     pass
    for user in User.user_list:
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
    for user in User.user_list:
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
    return jsonify(message)


@bp.route('/api/auth/reset-password', methods=['POST'])
def reset_password(old_password, new_password):
    pass


@bp.route('businesses', methods=['POST'])
def register_business():
    data = request.get_json()
    owner_email = data['owner_email']
    owner = User.get_user_by_email(owner_email, User.user_list)
    if owner is not None:
        business = Business(data['business_id'], data['owner_email'], data['name'], data['location'], data['profile'])
        businesses.append(business)
        message = {
                    'business': data['business_id'],
                    'status':'registered successfully'
                  }
        response = jsonify(message)
        response.status_code = 201
        return response
    message = {
        'business': data['business_id'],
        'status': 'User Unknown'
    }
    response = jsonify(message)
    response.status_code = 500
    return response


@bp.route('/api/businesses/<businessId>', methods=['PUT'])
def update_business_profile():
    pass


@bp.route ('/api/businesses/<businessId>', methods=['DELETE'])
def delete_business():
    pass


@bp.route ('all/businesses', methods=['GET'])
def retrieve_businesses():
    data = {}
    business_no = 1
    for business in businesses:
        business_data = {
            'id':business.id,
            'name':business.name,
            'locstion': business.location,
            'profile':business.profile
        }
        data[business_no]=business_data
        business_no += 1
    response = jsonify(data)
    response.status_code = 200
    return response


@bp.route('/api/businesses/<businessId>', methods=['GET'])
def get_a_business():
    pass


@bp.route('/api/businesses/<businessId>/reviews', methods=['POST'])
def add_review():
    pass


@bp.route('/api/businesses/<businessId>/reviews', methods=['GET'])
def get_reviews():
    pass
