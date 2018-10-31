'''user_endpoints.py contains endpoints for register,login and logout'''
import random

import re
from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_raw_jwt, get_jwt_claims, get_jwt_identity)
from ..models import user_model, blacklist_model
from ..utils import list_iterator

auth = Blueprint('auth', __name__, url_prefix='/api/v2')


user_object = user_model.User()


@auth.route('/register', methods=['POST'])
@jwt_required
def register():
    '''endpoint to add  a new user'''
    data = request.get_json()
    if not data:
        return jsonify({"message": "Fields cannot be empty"}), 400
    username = data.get('username').strip()
    name = data.get('name')
    email = data.get('email').strip()
    password = data.get('password').strip()
    confirm_password = data.get('confirm_password').strip()
    role = data.get('role').lower().strip()
    roles = ["admin", "attendant"]
    if role not in roles:
        return jsonify({"message": "The role {} does not exist.Only admin and attendant roles are allowed".format(role)}), 400

    userinfo = [username, name, role, password, confirm_password, email]

    exists = list_iterator(userinfo)
    if exists is False:
        return jsonify({"message": "Make sure all fields have been filled out"}), 206
    if len(password) < 4:
        return jsonify({"message": "The password is too short,minimum length is 4"}), 400
    if confirm_password != password:
        return jsonify({"message": "The passwords you entered don't match"}), 400
    match = re.match(
        r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match is None:
        return jsonify({"message": "Enter a valid email address"}), 403
    claims = get_jwt_claims()
    admin = "admin"
    if claims["role"] != admin:
        return jsonify({"message": "Only an admin can add new users!"}), 401
    response = jsonify(user_object.put(name, username, email, password, role))
    response.status_code = 201
    return response


@auth.route('/login', methods=['POST'])
def login():
    '''login user by verifying password and creating an access token'''
    data = request.get_json()
    if not data:
        return jsonify({"message": "Fields cannot be empty"}), 400
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"message": "Username or password missing"}), 206
    authorize = user_object.verify_password(username, password)
    user = user_object.get_user_by_username(username)
    if authorize == "True":
        access_token = create_access_token(identity=user)
        return jsonify(dict(token=access_token, message="Login successful!Welcome back, " + username + "!")), 200

    response = jsonify(authorize)
    response.status_code = 401
    return response


@auth.route('/logout', methods=['POST'])
@jwt_required
def logout():
    '''logout user by revoking password'''
    json_token_identifier = get_raw_jwt()['jti']
    revoked_token = blacklist_model.RevokedTokens()
    revoked_token.add_to_blacklist(json_token_identifier)
    return jsonify({"message": "Successfully logged out"}), 200


@auth.route('/users', methods=['GET'])
def get_all_users():
    '''Endpoint to get all users'''
    response = jsonify(user_object.get_all_users())
    response.status_code = 200
    return response


@auth.route('/users/<username>', methods=['GET'])
def get_user_by_username(username):
    '''Endpoint to get a  user by username'''
    response = jsonify(user_object.get_user_by_username(username))
    response.status_code = 200
    return response


@auth.route('/users/<username>', methods=['PUT'])
@jwt_required
def promote_demote_user(username):
    '''Endpoint to promote or demote a user'''
    identity = get_jwt_identity()
    admin = 'defaultadmin'
    if identity != admin:
        return jsonify({"message": "Only an super admin edit user roles"}), 401
    response = jsonify(user_object.promote_demote_user(username))
    response.status_code = 200
    return response
