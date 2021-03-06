from flask import Flask, request, jsonify, Blueprint, json
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_claims, get_jwt_identity)
from ..models import sales_model


sale = Blueprint('sale', __name__, url_prefix='/api/v2')


sale_object = sales_model.Sales()


@sale.route('/sales', methods=['POST'])
@jwt_required
def post_sales():
    '''Endpoint for only attendant to post a sale'''
    created_by = get_jwt_identity()
    claims = get_jwt_claims()
    attendant = "attendant"
    if claims["role"] != attendant:
        return jsonify({"message": "Only an attendant is permitted to post sales"}), 401
    response = jsonify(sale_object.put(created_by))
    response.status_code = 201
    return response


@sale.route('/sales', methods=['GET'])
@jwt_required
def get_all_sales():
    '''Endpoint for only admin to view all sales'''
    claims = get_jwt_claims()
    admin = "admin"
    if claims["role"] != admin:
        return jsonify({"message": "Only an admin can view all sales records"}), 401
    response = jsonify(sale_object.get_all_sales())
    response.status_code = 200
    return response


@sale.route('/sales/<int:sale_id>', methods=['GET'])
@jwt_required
def get_sale_by_id(sale_id):
    '''Endpoint for only admin or creator of sale to  view a sale'''
    claims = get_jwt_claims()
    identity = get_jwt_identity()
    creator = sale_object.get_who_created_sale(sale_id)
    admin = "admin"
    if claims["role"] != admin and creator != identity:
        return jsonify({"message": "Only an admin or attendant who created this sale are allowed to view it"}), 401
    response = jsonify(sale_object.get_sale_by_id(sale_id))
    response.status_code = 200
    return response
