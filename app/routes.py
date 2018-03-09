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
        Business.businesses.append(business)
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
    for business in Business.businesses:
        data[business_no]=business.__repr__()
        business_no += 1
    response = jsonify(data)
    response.status_code = 200
    return response


@bp.route('businesses/<int:business_id>', methods=['GET'])
def get_a_business(business_id, **kwargs):
    business = Business.get_business(business_id)
    if business is not None:
        response = jsonify(business.__repr__())
        response.status_code = 201
        return response
    message = {'status':'Object not found'}
    response = jsonify(message)
    response.status_code = 400
    return response


@bp.route('businesses/<int:businessId>/reviews', methods=['POST'])
def add_review(businessId, **kwargs):
    data = request.get_json()
    review = Review(data['review_id'], businessId, data['user_id'], data['review_text'])
    business = Business.get_business(businessId)
    user = User.get_user(data['user_id'])
    if business and user is not None:
        business.reviews.append(review)
        Review.reviews.append(review)
        response = jsonify({'review':review.__repr__(),
                            'status':'added successfuly'
                            })
        response.status_code = 201
        return response
    response = jsonify({
                        'review':review.__repr__(),
                        'status':'review cannot be added, User or bsiness invalid'
                        })
    response.status_code = 300
    return response


@bp.route('businesses/<int:businessId>/all/reviews', methods=['GET'])
def get_reviews(businessId, **kwargs):
    business = Business.get_business(businessId)
    data = {}
    review_no = 1
    if business is not None:
        for review in business.reviews:
            data[review_no] = review.__repr__()
            review_no += 1
        response = jsonify(data)
        response.status_code = 200
        return response
    response = {
                'message':'No such business or review'
                }
