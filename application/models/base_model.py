'''app/models/base_models.py'''
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from instance.config import app_config
from manage import DbSetup



CURRENT_ENVIRONMENT= os.environ['ENV']
CONN_STRING = app_config[CURRENT_ENVIRONMENT].CONNECTION_STRING
class BaseModel(object):
    
    def __init__(self):
        '''open database connections'''
        self.conn = psycopg2.connect(CONN_STRING)
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def select_with_condition(self, table, column, param):
        '''select based on a condition'''
        query = 'SELECT * FROM {} WHERE {} =%s'.format(table, column)
        self.cursor.execute(query, (param,))
        list_ = self.cursor.fetchone()
        if list_:
            return list_
        return {"message": "{} does not exist in our records".format(column)}

    def select_no_condition(self, table, column):
        '''select based on no condition'''
        query = 'SELECT * FROM {} ORDER BY {} ASC'.format(table, column)
        self.cursor.execute(query)
        list_ = self.cursor.fetchall()
        if list_:
            return list_
        return {"message": "There are no {} records".format(table)}
