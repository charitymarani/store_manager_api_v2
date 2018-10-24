from unittest import TestCase


class BaseTestCase(TestCase):

    def setUp(self):

        self.register_data = dict(
            name='charity marani',
            email='amina@gmail.com',
            role='admin',
            username='amina',
            password='1234',
            confirm_password='1234'
        )
        self.login_data = dict(username='amina',
                               password='1234'
                               )
        self.product_data = dict(product_id='100',
                                 name='heels',
                                 category='shoes',
                                 quantity='50',
                                 description=' a shoe with raisedd heel')

    def tearDown(self):
        pass
