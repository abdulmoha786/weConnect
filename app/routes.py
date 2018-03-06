from flask import url_for, request, jsonify
from app import app
from app.models import User, Business, Review


@app.route('/api/auth/register', methods=['POST'])
def create_user():
    # content = request.get_json(force=True)
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    user_id = data['user_id']
    user = User()
    message = user.create_user(user_id, username, email, password)

    return jsonify(message)


@app.route ('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json ()
    for user in User.users:
        usr = User(user['use_id'],user['username'],user['email'],user['password'])
        if user['username'] == data['username'] and usr.check_password(data['password']):
            usr.login = True
            message = {
                        'user':data['username'],
                        'message':"Login Successful"
                        }
            return jsonify(message)
    message = {
                'user': data['username'],
                'message': "Login Unsuccessful"
                }
    return jsonify(message)


@app.route ('/api/auth/login', methods=['POST'])
def logout():
    pass


@app.route ('/api/auth/reset-password', methods=['POST'])
def reset_password(old_password, new_password):
    pass


@app.route ('/api/businesses', methods=['POST'])
def register_business(old_password, new_password):
    pass


@app.route ('/api/businesses/<businessId>', methods=['PUT'])
def update_business_profile():
    pass


@app.route ('/api/businesses/<businessId>', methods=['DELETE'])
def delete_business():
    pass


@app.route ('/api/businesses', methods=['GET'])
def retrieve_businesses(old_password, new_password):
    pass


@app.route ('/api/businesses/<businessId>', methods=['GET'])
def get_a_business():
    pass


@app.route ('/api/businesses/<businessId>/reviews', methods=['POST'])
def add_review():
    pass


@app.route ('/api/businesses/<businessId>/reviews', methods=['GET'])
def get_reviews():
    pass
