
'''instance/config.py'''
import os


class Config(object):
    '''parent config file'''
    DEBUG = True
    SECRET_KEY = os.urandom(24)


class Development(Config):
    '''Configurations for development'''
    DEBUG = True
    CONNECTION_STRING = "dbname = 'store_manager' host = 'localhost' user = 'postgres'"


class Testing(Config):
    '''configurations for testing with a separate test database'''
    TESTING = True
    DEBUG = True
    CONNECTION_STRING = "dbname = 'test_store_db' host = 'localhost' user = 'postgres'"
    


app_config = {
    'development': Development,
    'testing': Testing
}
