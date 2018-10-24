
import json
from tests.base_tests import BaseTestCase


class TestAuthentication(BaseTestCase):

    def test_registration(self):
        with self.client:
            
            # Test register
            response = self.client.post(
                self.signupurl,
                data=json.dumps(self.register_data),
                content_type='application/json'
            )
            response_data1 = json.loads(response.data)
            self.assertEqual(
                "Welcome amina!", response_data1["message"])
            self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        with self.client:
            # Register a user
            self.client.post(
                self.signupurl,
                data=json.dumps(self.register_data),
                content_type='application/json'
            )
            # Test for successful Login
            response = self.client.post(
                self.loginurl,
                data=json.dumps(self.login_data),
                content_type='application/json'
            )
            response_data1 = json.loads(response.data)
            self.assertEqual(
                "Login successful!Welcome back,amina!", response_data1["message"])
            self.assertEqual(response.status_code, 200)

     

