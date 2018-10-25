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
        self.manage = DbSetup()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.signupurl = '/api/v2/register'
        self.loginurl = '/api/v2/login'
        self.logouturl = '/api/v2/logout'
        self.allusersurl = '/api/v2/users'

        self.register_data = dict(
            name='charity marani',
            email='rodday@gmail.com',
            role='attendant',
            username='rodday',
            password='1234',
            confirm_password='1234'
        )
        self.login_data = dict(username='rodday',
                               password='1234'
                               )
        self.default_login = dict(username='defaultadmin',
                                  password='1234admin'
                                  )

    def tearDown(self):
        """removes the db and the context"""
        self.app_context.pop()
