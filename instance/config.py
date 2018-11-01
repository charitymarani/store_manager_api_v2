
'''instance/config.py'''
import os


class Config(object):
    '''parent config file'''
    DEBUG = True
    SECRET_KEY = os.urandom(24)
    CONNECTION_STRING = os.getenv('CONNECTION_STRING')
class Development(Config):
    '''Configurations for development'''
    DEBUG = True

class Testing(Config):
    '''configurations for testing with a separate test database'''
    TESTING = True
    DEBUG = True
    os.environ['ENV'] = 'testing'
    CONNECTION_STRING = "dbname = 'test_store_db' user = 'postgres' host ='localhost' port ='5432' password='chacha'"


app_config = {
    'development': Development,
    'testing': Testing
}
