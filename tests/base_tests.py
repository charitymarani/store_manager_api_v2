from unittest import TestCase
from application import create_app
from manage import DbSetup
from instance.config import app_config


class BaseTestCase(TestCase):

    def setUp(self):
        self.app = create_app(config='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.manage = DbSetup('testing')
        self.manage.drop_tables()
        self.manage.create_tables()
        self.manage.create_default_admin()
        

        self.signupurl='/api/v2/register'
        self.loginurl='/api/v2/login'
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
        self.manage.drop_tables()

    