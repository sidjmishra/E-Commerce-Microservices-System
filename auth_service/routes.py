from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
import configparser
import re

auth_bp = Blueprint('auth', __name__)

config = configparser.ConfigParser()
config.read("app.ini")
mongo_client = MongoClient(config["connections"]["MONGO_URI"])

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user_regex = "^[a-z]+(?:_[a-z]+)?$"
    if not re.match(user_regex, username):
        return jsonify({"message": "Username must be in lowercase, can only have one '_' as special character and atleast 4 characters in length!"}), 400
    
    if mongo_client.pest_tech.users.find_one({'username': username}):
        return jsonify({'message': 'User already exists'}), 409

    pass_regex = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    if not re.match(pass_regex, password):
        return jsonify({"message": "Password does not match the following: Password must be 8 characters long, at least 1 uppercase, at least 1 lowercase, at least 1 number and at least 1 special character: '#?!@$%^&*-'"}), 400

    hashed_password = generate_password_hash(password)
    mongo_client.pesto_tech.users.insert_one({'username': username, 'password_hash': hashed_password})
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = mongo_client.pesto_tech.users.find_one({'username': username})
    if user and check_password_hash(user['password_hash'], password):
        access_token = create_access_token(identity={'username': user['username']})
        return jsonify(access_token=access_token), 200
    return jsonify({'message': 'Invalid credentials'}), 401
