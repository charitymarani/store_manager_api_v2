import json
from .base_tests import BaseTestCase


def register(my_client):
    """Function that holds data for register"""
    resp_register = my_client.post(
        '/api/v2/auth/register',
        data=json.dumps(dict(
            name='charity marani',
            email='caro@gmail.com',
            role='admin',
            username='caro',
            password='1234',
            confirm_password='1234'
        )),
        content_type='application/json'
    )
    return resp_register


def login(my_client):
    """Function that holds data for login"""
    resp_login = my_client.post(
        '/api/v2/auth/register',
        data=json.dumps(dict(
            username='caro',
            password='1234'
        )),
        content_type='application/json'
    )
    result = json.loads(resp_login.data)
    token = result["token"]
    return token


class TestProducts(BaseTestCase):

    def test_edit_product(self):
        resp_register = register(self.client)
        token = login(self.client)
        result = self.client.post('/api/v2/products', headers=dict(Authorization="Bearer " + token), content_type="application/json",
                                  data=json.dumps(self.product_data))
        self.assertEqual(result.status_code, 201)
        result3 = self.client.put('/api/v2/products/100', headers=dict(Authorization="Bearer " + token),
                                  content_type="application/json", data=json.dumps({"name": "chunky heels"}))
        self.assertEqual(result3.status_code, 200)

    def test_delete_product(self):
        resp_register = register(self.client)
        token = login(self.client)
        result = self.client.post('/api/v2/products', headers=dict(Authorization="Bearer " + token), content_type="application/json",
                                  data=json.dumps(self.product_data))
        self.assertEqual(result.status_code, 201)
        result3 = self.client.delete('/api/v2/products/100', headers=dict(Authorization="Bearer " + token),
                                     content_type="application/json")
        self.assertEqual(result3.status_code, 200)
