import os
from manage import DbSetup
from instance.config import app_config

CURRENT_ENVIRONMENT = os.environ['ENV']
CONN_STRING = app_config[CURRENT_ENVIRONMENT].CONNECTION_STRING
conn = psycopg2.connect(CONN_STRING)
cur = conn.cursor()


def list_iterator(list_):
    for listitem in list_:
        if listitem is None or not listitem:
            return False


def select_with_condition(table, column, param):
    '''select based on a condition'''
    query = 'SELECT * FROM {} WHERE {} =%s'.format(table, column)
    cur.execute(query, (param,))
    list_ = cur.fetchone()
    if list_:
        return list_
    return {"message": "{} does not exist in our records".format(column)}


def select_no_condition(table, column):
    '''select based on no condition'''
    query = 'SELECT * FROM {} ORDER BY {} ASC'.format(table, column)
    cur.execute(query)
    list_ = cur.fetchall()
    if list_:
        return list_
    return {"message": "There are no {} records".format(table)}
