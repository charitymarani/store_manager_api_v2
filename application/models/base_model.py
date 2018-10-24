'''app/models/base_models.py'''
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from instance.config import app_config
from manage import DbSetup

CONFIG="development"
CONN_STRING = app_config[CONFIG].CONNECTION_STRING

class BaseModel(object):

    def __init__(self):
        '''open database connections'''
        self.conn = psycopg2.connect(CONN_STRING)
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    
