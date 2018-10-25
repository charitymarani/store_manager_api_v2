import os
import psycopg2

import unittest
from application import create_app, my_db
from manage import DbSetup
from instance.config import app_config


class Testbase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context=self.app.app_context()
        self.app_context.push()
        # my_db.create_tables()
        # my_db.create_default_admin()
        self.signupurl = '/api/v2/register'
        self.loginurl = '/api/v2/login'
        self.register_data = dict(
            name='charity marani',
            email='rodda@gmail.com',
            role='attendant',
            username='rodda',
            password='1234',
            confirm_password='1234'
        )
        self.login_data = dict(username='rodda',
                               password='1234'
                               )
        self.default_login = dict(username='defaultadmin',
                                  password='1234admin'
                                  )

    def tearDown(self):
        """removes the db and the context"""
        self.app_context.pop()
        # my_db.drop_tables()
        # current_environemt = os.environ['ENV']
        # conn_string = app_config[current_environemt].CONNECTION_STRING
        # conn = psycopg2.connect(conn_string)
        # cursor = conn.cursor()
        # cursor.execute("""DROP TABLE users, products, sales, blacklist""")
        # conn.commit()
        # conn.close()
