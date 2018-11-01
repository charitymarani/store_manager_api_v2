import os
import psycopg2
import unittest
import json
from application import create_app
from manage import DbSetup
from instance.config import app_config


class Testbase(unittest.TestCase):
    db = DbSetup(config_name='testing')
    db.drop_tables()
    def setUp(self):
        '''Setup function for tests'''
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()

        with self.app_context:
            self.app_context.push()

        self.signupurl = '/api/v2/register'
        self.loginurl = '/api/v2/login'
        self.logouturl = '/api/v2/logout'
        self.allusersurl = '/api/v2/users'
        self.producturl = '/api/v2/products'
        self.salesurl='/api/v2/sales'
        self.carturl='/api/v2/carts'

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
        self.register_data2 = dict(
            name='charity marani',
            email='mose@gmail.com',
            role='attendant',
            username='mose',
            password='1234',
            confirm_password='1234'
        )
        self.login_data2 = dict(username='mose',
                                password='1234'
                                )
        self.register_data3= dict(
            name='charity marani',
            email='geb@gmail.com',
            role='attendant',
            username='geb',
            password='1234',
            confirm_password='1234'
        )
        self.register_data4 = dict(
            name='charity marani',
            email='nicoleb@gmail.com',
            role='attendant',
            username='nicoleb',
            password='1234',
            confirm_password='1234'
        )
        self.register_data5 = dict(
            name='charity marani',
            email='aim@gmail.com',
            role='attendant',
            username='aim',
            password='1234',
            confirm_password='1234'
        )

        self.login_data4 = dict(username='nicoleb',
                               password='1234'
                               )
        self.login_data3 = dict(username='geb',
                                password='1234'
                                )
        self.default_login = dict(username='defaultadmin',
                                  password='1234admin'
                                  )
        self.productdata = dict(
            product_code=120,
            name='scarf',
            category='clothes',
            purchase_price=1000,
            selling_price=1800,
            quantity=70,
            low_limit=10,
            description='A warm cloth'

        )
        self.productdata2 = dict(
            product_code=130,
            name='pen',
            category='shoes',
            purchase_price=1000,
            selling_price=1800,
            quantity=70,
            low_limit=10,
            description='writing tool'

        )
        self.productdata3 = dict(
            product_code=140,
            name='phone',
            category='electronics',
            purchase_price=1000,
            selling_price=1800,
            quantity=70,
            low_limit=10,
            description='communication device'

        )
        self.productdata4 = dict(
            product_code=150,
            name='earphones',
            category='electronics',
            purchase_price=1000,
            selling_price=1800,
            quantity=70,
            low_limit=10,
            description='communication device'

        )
        
        self.edit_data = dict(quantity=70,
                              low_limit=10,
                              description='wide based heel')
        self.empty_data_fields = dict(name="",
                                      category=""
                                      )
        self.cart_data=dict(
                    quantity=4,
                    cart_item="scarf"
                )
        self.cart_data1=dict(
                    quantity=4,
                    cart_item="pen"
                )
        self.cart_data2=dict(
                    quantity=4,
                    cart_item="earphones"
                )
        self.no_cart_item=dict(
                    quantity=4,
                    cart_item="book"
                )
   
                


    def tearDown(self):
        """removes the db and the context"""
        with self.app_context:
            self.app_context.pop()
            