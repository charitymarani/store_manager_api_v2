from flask import Flask, request, jsonify,Blueprint,json
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_claims)
from ..models import product_model
from ..utils import list_iterator

product = Blueprint('product', __name__,url_prefix='/api/v2')


product_object = product_model.Products()

@product.route('/products',methods=['POST'])
@jwt_required
def post_product():
    '''Endpoint for only an admin to post a product'''
    data=request.get_json()
    if not data:
        return jsonify({"message": "Fields cannot be empty"}),400 
    product_id=data.get("product_id")
    name=data.get("name")
    category=data.get("category")
    B_price=data.get("purchase_price")
    S_price=data.get("selling_price")
    qty=data.get("quantity")
    limit=data.get("low_limit")
    desc=data.get("description")

    productinfo=[product_id,name,qty,limit,S_price]
    exists = list_iterator(productinfo)
    if exists is False:
        return jsonify({"message": "Some required fields are missing!"}) ,206
    claims=get_jwt_claims()
    admin="admin"
    if claims['role'] != admin:
        return jsonify({"message":"Only an admin is permitted to post products"}),401
    response=jsonify(product_object.put(product_id, name, category, B_price,S_price,qty,limit,desc))

    response.status_code = 201
    return response 
@product.route('/products',methods=['GET']) 
@jwt_required
def get_all_products():
    '''Endpoint to get all products'''
    response=jsonify(product_object.get_all_products())
    response.status_code=200
    return response
@product.route('/products/<int:product_id>',methods=['GET']) 
@jwt_required
def get_product_by_id(product_id):
    '''Endpoint to get product by product id'''
    response=jsonify(product_object.get_product_by_id(product_id))
    response.status_code=200
    return response