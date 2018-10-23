import json
from .base_tests import BaseTestCase


class TestAuth(BaseTestCase):

    def test_registration(self):

        # Test successful registration
        response = self.client.post(
            '/api/v1/auth/register',
            data=json.dumps(self.register_data),
            content_type='application/json'
        )
        response_data = json.loads(response.data)
        self.assertEqual(
            "User with username amina added successfully", response_data["message"])
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):

        # Register a user
        self.client.post(
            '/api/v1/auth/register',
            data=json.dumps(self.register_data),
            content_type='application/json'
        )
        # Test for successful Login
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps(self.login_data),
            content_type='application/json'
        )
        response_data = json.loads(response.data)
        self.assertEqual("Login successful!", response_data["message"])
        self.assertEqual(response.status_code, 200)
