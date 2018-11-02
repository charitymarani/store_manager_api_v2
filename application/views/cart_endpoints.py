from flask import Flask, request, jsonify, Blueprint, json
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_claims, get_jwt_identity)
from ..models import cart_model
from ..utils import list_iterator,check_is_int

cart = Blueprint('cart', __name__, url_prefix='/api/v2')
cart_object = cart_model.Carts()

@cart.route('/carts', methods=['POST'])
@jwt_required
def post_to_cart():
    '''Endpoint for only attendant to post a sale'''
    data = request.get_json()
    if not data:
        return jsonify({"message": "Fields cannot be empty"}), 400
    items_count = data.get("quantity")
    item = data.get("cart_item")
    created_by = get_jwt_identity()
    cartinfo = [items_count, item]
    cart_int=[items_count]
    is_int=check_is_int(cart_int)
    for item in cartinfo:
        if item is None or not item:
            return jsonify({"message": "{} field can't be empty".format(item)}), 206
    if is_int is True:
        claims = get_jwt_claims()
        attendant = "attendant"
        if claims["role"] != attendant:
            return jsonify({"message": "Only an attendant is permitted to add to cart"}), 401
        response = jsonify(cart_object.put(created_by, item, items_count))
        response.status_code = 201
        return response
    return is_int


@cart.route('/carts', methods=['GET'])
@jwt_required
def get_all_cart():
    '''Endpoint for only attendant to view the cart'''
    claims = get_jwt_claims()
    creator = get_jwt_identity()
    attendant = "attendant"
    if claims["role"] != attendant:
        return jsonify({"message": "Only an attendant can view cart items"}), 401
    response = jsonify(cart_object.get_all_cart_items(creator))
    response.status_code = 200
    return response


@cart.route('/carts/<int:cart_item_id>', methods=['DELETE'])
@jwt_required
def delete_cart_item(cart_item_id):
    claims = get_jwt_claims()
    attendant = "attendant"
    if claims["role"] != attendant:
        return jsonify({"message": "Only an attendant can delete cart items"}), 401
    response = jsonify(cart_object.delete_cart_item(cart_item_id))
    response.status_code = 200
    return response


@cart.route('/carts', methods=['DELETE'])
@jwt_required
def delete_cart():
    claims = get_jwt_claims()
    creator = get_jwt_identity()
    attendant = "attendant"
    if claims["role"] != attendant:
        return jsonify({"message": "Only an attendant can delete a cart items"}), 401
    response = jsonify(cart_object.delete_cart(creator))
    response.status_code = 200
    return response


@cart.route('/carts/<int:cart_item_id>', methods=['PUT'])
@jwt_required
def update_cart(cart_item_id):
    claims = get_jwt_claims()
    identity = get_jwt_identity()
    creator = cart_object.get_cart_item_by_id(cart_item_id)["created_by"]
    print(creator)
    attendant = "attendant"
    if claims["role"] != attendant and identity != creator:
        return jsonify({"message": "Only an attendant who added to cart can update a cart item"}), 401
    data = request.get_json()
    print(data)
    count = data.get('quantity')
    cart_int=[count]
    is_int=check_is_int(cart_int)
    if is_int is True:
        response = jsonify(cart_object.update_cart_item(cart_item_id, count))
        response.status_code = 200
        return response
    return is_int
