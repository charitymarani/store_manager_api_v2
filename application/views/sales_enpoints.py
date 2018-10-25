from flask import Flask, request, jsonify,Blueprint,json
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_claims,get_jwt_identity)
from ..models import sales_model


sale = Blueprint('sale', __name__,url_prefix='/api/v2')


sale_object = sales_model.Sales()

@sale.route('/sales',methods=['POST'])
@jwt_required
def post_sales():
    '''Endpoint for only attendant to post a sale'''
    data=request.get_json()
    if not data:
        return jsonify({"message": "Fields cannot be empty"}),400 
    items_count=data.get("items_count")
    items=data.get("items")
    price=data.get("price")
    created_by=get_jwt_identity()
    salesinfo=[items_count,price,items]
    for item in salesinfo:
        if item is None or not item:
            return jsonify({"message":"Items_count and total_amount fields can't be empty"}),206
    claims=get_jwt_claims()
    attendant="attendant"
    if claims["role"] != attendant:
        return jsonify({"message":"Only an attendant is permitted to post sales"}),401
    response=jsonify(sale_object.put(created_by,items,items_count,price))
    response.status_code=201
    return response
    
@sale.route('/sales',methods=['GET'])
@jwt_required
def get_all_sales():
    '''Endpoint for only admin to view all sales'''
    claims=get_jwt_claims()
    admin="admin"
    if claims["role"]!= admin:
        return jsonify({"message":"Only an admin can view all sales records"}),401
    response= jsonify(sale_object.get_all_sales())
    response.status_code=200
    return response

