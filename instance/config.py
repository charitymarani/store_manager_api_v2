
'''instance/config.py'''
import os
class Config(object):
    '''parent config file'''
    DEBUG = True
    SECRET_KEY = os.urandom(24)
  

class Development(Config):
    '''Configurations for development'''
    DEBUG = True
    os.environ['DB_NAME'] = 'store_manager'
    os.environ['DB_USER'] = 'postgres'
    os.environ['DB_PASSWORD'] = 'chacha'
    os.environ['DB_HOST'] = 'localhost'


class Testing(Config):
    '''configurations for testing with a separate test database'''
    TESTING = True
    DEBUG = True
    os.environ['DB_NAME'] = 'test_store_db'
    os.environ['DB_USER'] = 'postgres'
    os.environ['DB_PASSWORD'] = 'chacha'
    os.environ['DB_HOST'] = 'localhost'

app_config = {
    'development' : Development,
    'testing' : Testing
}
