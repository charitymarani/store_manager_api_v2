
'''application/__init__.py'''
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from instance.config import app_config
from .views.user_endpoints import auth
from manage import DbSetup



def create_app(config):
    '''function configuring the Flask App'''
    # os.environ['ENV']= config
    from .models.blacklist_model import RevokedTokens
    
    my_db = DbSetup()
    my_db.create_tables()
    my_db.create_default_admin()
    
    app = Flask(__name__)
    CORS(app)

    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config])
    app.config['TESTING']= True

    app.config['JWT_SECRET_KEY'] = 'mysecretkey'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    jwt = JWTManager(app)

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

   
    return app
