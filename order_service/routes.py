from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from flask_jwt_extended import jwt_required, get_jwt_identity
import configparser

order_bp = Blueprint('orders', __name__)

config = configparser.ConfigParser()
config.read("app.ini")
mongo_client = MongoClient(config["connections"]["MONGO_URI"])

@order_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()
    user_id = get_jwt_identity()['username']
    new_order = {
        'user_id': user_id,
        'product_id': data['product_id'],
        'quantity': data['quantity'],
        'total_price': data['total_price'],
        'status': 'pending'
    }
    mongo_client.pesto_tech.orders.insert_one(new_order)
    new_order['_id'] = str(new_order['_id'])
    return jsonify(new_order), 201

@order_bp.route('/<string:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    from bson.objectid import ObjectId
    order = mongo_client.pesto_tech.orders.find_one({'_id': ObjectId(order_id)})
    
    if order:
        order['_id'] = str(order['_id'])
        return jsonify(order), 200

    return jsonify({"message": "No such order available"}), 404

@order_bp.route('/user/<string:user_id>', methods=['GET'])
@jwt_required()
def get_user_orders(user_id):
    orders = list(mongo_client.pesto_tech.orders.find({'user_id': user_id}))
    for order in orders:
        order['_id'] = str(order['_id'])
    return jsonify(orders), 200

@order_bp.route('/<string:order_id>', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    from bson.objectid import ObjectId
    data = request.get_json()
    update_fields = {}
    if 'status' in data:
        update_fields['status'] = data['status']
    
    mongo_client.pesto_tech.orders.update_one({'_id': ObjectId(order_id)}, {'$set': update_fields})
    order = mongo_client.pesto_tech.orders.find_one({'_id': ObjectId(order_id)})
    order['_id'] = str(order['_id'])
    return jsonify(order), 200
