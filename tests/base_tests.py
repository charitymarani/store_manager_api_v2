import os
import psycopg2

import unittest
from application import create_app, my_db
from manage import DbSetup
from instance.config import app_config

db = DbSetup()


class Testbase(unittest.TestCase):

    def setUp(self):

        self.app = create_app('testing')
        self.client = self.app.test_client()

        # db.create_tables()

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.signupurl = '/api/v2/register'
        self.loginurl = '/api/v2/login'
        self.logouturl = '/api/v2/logout'
        self.allusersurl = '/api/v2/users'
        self.producturl = '/api/v2/products'

        self.register_data = dict(
            name='charity marani',
            email='nicole@gmail.com',
            role='attendant',
            username='nicole',
            password='1234',
            confirm_password='1234'
        )
        self.login_data = dict(username='nicole',
                               password='1234'
                               )
        self.register_data1 = dict(
            name='charity marani',
            email='kim@gmail.com',
            role='attendant',
            username='kim',
            password='1234',
            confirm_password='1234'
        )
        self.login_data1 = dict(username='kim',
                               password='1234'
                               )
        self.default_login = dict(username='defaultadmin',
                                  password='1234admin'
                                  )
        self.productdata = dict(
            product_id=504,
            name='chunky heels',
            category='shoes',
            purchase_price=1000,
            selling_price=1800,
            quantity=70,
            low_limit=10,
            description='A wide based heel'

        )
        self.productdata2=dict(
                    product_id=200,
                    name='chunky heels',
                    category='shoes',
                    purchase_price=1000,
                    selling_price=1800,
                    quantity=70,
                    low_limit=10,
                    description='A wide based heel'

                )
    def tearDown(self):
        """removes the db and the context"""
        self.app_context.pop()
        # db.drop_tables()
