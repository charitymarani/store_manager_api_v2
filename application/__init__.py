
'''application/__init__.py'''
import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from instance.config import app_config
from flask_mail import Mail
from .views.user_endpoints import auth
from .views.product_endpoints import product
from .views.sales_enpoints import sale
from .views.cart_endpoints import cart
from manage import DbSetup

mail=Mail()

def create_app(config_name):
    '''function configuring the Flask App'''

    from .models.blacklist_model import RevokedTokens
    from .error_handlers import resource_not_found, method_not_allowed, bad_request
    password=os.getenv('password')
    app = Flask(__name__)

    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'mysecretkey'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'defaultstore001'
    app.config['MAIL_DEFAULT_SENDER'] = 'defaultstore001@gmail.com'
    app.config['MAIL_PASSWORD'] = password
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    jwt = JWTManager(app)
    mail=Mail(app)
   
    @jwt.user_claims_loader
    def add_claims_to_access_token(user_object):
        '''add role claims to access token'''
        return {'role': user_object['role']}

    @jwt.user_identity_loader
    def user_identity_lookup(user_object):
        '''set token identity from user_object passed to username'''
        return user_object["username"]

    @jwt.token_in_blacklist_loader
    def check_if_token_blacklist(decrypted_token):
        '''check if jti(unique identifier) is in black list'''
        json_token_identifier = decrypted_token['jti']
        revoked_tokens = RevokedTokens()
        return revoked_tokens.is_jti_blacklisted(json_token_identifier)

    app.register_blueprint(auth)
    app.register_blueprint(product)
    app.register_blueprint(sale)
    app.register_blueprint(cart)
    app.register_error_handler(404, resource_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(400, bad_request)

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        return jsonify(dict(error='Your request cannot be proccessed. the server experienced an internal error')), 500

    my_db = DbSetup(config_name)
    my_db.create_tables()
    my_db.create_default_admin()

    return app
