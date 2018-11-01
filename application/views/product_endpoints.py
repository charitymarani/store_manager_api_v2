from flask import Flask, request, jsonify, Blueprint, json
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_claims)
from ..models import product_model
from ..utils import list_iterator, check_is_int

product = Blueprint('product', __name__, url_prefix='/api/v2')
product_object = product_model.Products()

@product.route('/products', methods=['POST'])
@jwt_required
def post_product():
    '''Endpoint for only an admin to post a product'''
    data = request.get_json()
    if not data:
        return jsonify({"message": "Fields cannot be empty"}), 400
    product_code = data.get("product_code")
    name = data.get("name")
    category = data.get("category")
    B_price = data.get("purchase_price")
    S_price = data.get("selling_price")
    qty = data.get("quantity")
    limit = data.get("low_limit")
    desc = data.get("description")

    productinfo = [product_code, name, qty,
                   limit, S_price, category, B_price, desc]
    product_int = [product_code, B_price, S_price, qty, limit]
    check_is_int(product_int)
    exists = list_iterator(productinfo)
    if exists is False:
        return jsonify({"message": "Some required fields are missing!"}), 206
    claims = get_jwt_claims()
    admin = "admin"
    if claims['role'] != admin:
        return jsonify({"message": "Only an admin is permitted to post products"}), 401
    response = jsonify(product_object.put(
        product_code, name, category, B_price, S_price, qty, limit, desc))
    response.status_code = 201
    return response


@product.route('/products', methods=['GET'])
@jwt_required
def get_all_products():
    '''Endpoint to get all products'''
    response = jsonify(product_object.get_all_products())
    response.status_code = 200
    return response


@product.route('/products/<int:product_code>', methods=['GET'])
@jwt_required
def get_product_by_id(product_code):
    '''Endpoint to get product by product id'''
    response = jsonify(product_object.get_product_by_id(product_code))
    response.status_code = 200
    return response


@product.route('/products/<int:product_code>', methods=['PUT'])
@jwt_required
def edit_product(product_code):
    '''Only admin can edit a product'''
    claims = get_jwt_claims()
    admin = "admin"
    if claims["role"] == admin:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Fields cannot be empty"}), 400
        name = data.get("name")
        category = data.get("category")
        B_price = data.get("purchase_price")
        S_price = data.get("selling_price")
        qty = data.get("quantity")
        limit = data.get("low_limit")
        desc = data.get("description")

        product = product_object.get_product_by_id(product_code)
        if "message" in product:
            return jsonify({"message": "Product does not exist"})
        if not name and not category and not B_price and not S_price and not qty and not limit and not desc:
            return jsonify({"message": "All fields cannot be empty enter data to edit"}), 400
        if not name:
            name = product["name"]
        if not category:
            category = product["category"]
        if not B_price:
            B_price = product["purchase_price"]
        if not S_price:
            S_price = product["selling_price"]
        if not qty:
            qty = product["quantity"]
        if not limit:
            limit = product["low_limit"]
        if not desc:
            desc = product["description"]

        response = jsonify(product_object.update_product(
            product_code, name, category, B_price, S_price, qty, limit, desc))

        response.status_code = 200
        return response
    return jsonify({"message": "Only admin can edit a product"}), 401


@product.route('/products/<int:product_code>', methods=['DELETE'])
@jwt_required
def delete_product(product_code):
    claims = get_jwt_claims()
    admin = "admin"
    if claims["role"] == admin:
        result = jsonify(product_object.delete_product(product_code))
        result.status_code = 200
        return result
    return jsonify({"message": "Only admin can delete a product"}), 401

