from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from flask_jwt_extended import jwt_required
import configparser

product_bp = Blueprint('products', __name__)

config = configparser.ConfigParser()
config.read("app.ini")
mongo_client = MongoClient(config["connections"]["MONGO_URI"])

@product_bp.route('/', methods=['GET'])
def get_products():
    products = list(mongo_client.pesto_tech.products.find())

    if len(products) < 0:
        return jsonify({"message": "No products available"}), 404

    for product in products:
        product['_id'] = str(product['_id'])
    return jsonify(products), 200

@product_bp.route('/<string:product_id>', methods=['GET'])
def get_product(product_id):
    from bson.objectid import ObjectId
    product = mongo_client.pesto_tech.products.find_one({'_id': ObjectId(product_id)})
    if product:
        product['_id'] = str(product['_id'])
        return jsonify(product), 200
    return jsonify({"message": "No such product available"}), 404

@product_bp.route('/create_product', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    new_product = {
        'name': data['name'],
        'description': data['description'],
        'price': data['price'],
        'stock': data['stock'],
        'version': 0
    }
    mongo_client.pesto_tech.products.insert_one(new_product)
    new_product['_id'] = str(new_product['_id'])
    return jsonify({"message": "Product added successfully", "product": new_product}), 201

@product_bp.route('/<string:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    from bson.objectid import ObjectId
    data = request.get_json()
    update_fields = {}
    if 'name' in data:
        update_fields['name'] = data['name']
    if 'description' in data:
        update_fields['description'] = data['description']
    if 'price' in data:
        update_fields['price'] = data['price']
    if 'stock' in data:
        update_fields['stock'] = data['stock']

    update_fields['version'] = mongo_client.pesto_tech.products.find_one({'_id': ObjectId(product_id)})['version'] + 1

    mongo_client.pesto_tech.products.update_one({'_id': ObjectId(product_id)}, {'$set': update_fields})
    product = mongo_client.pesto_tech.products.find_one({'_id': ObjectId(product_id)})
    product['_id'] = str(product['_id'])
    return jsonify({"message": "Product updates successfully", "product": product}), 200

@product_bp.route('/<string:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    from bson.objectid import ObjectId
    mongo_client.pesto_tech.products.delete_one({'_id': ObjectId(product_id)})
    return jsonify({'message': 'Product deleted successfully'}), 200