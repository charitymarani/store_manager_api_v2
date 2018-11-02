import json
from .base_tests import Testbase


class TestErrors(Testbase):
    def login_default_admin(self):

        response1 = self.client.post(self.loginurl, data=json.dumps(self.default_login),
                                     content_type='application.json')
        result = json.loads(response1.data)
        token = result["token"]

        return token

    def test_404(self):
        with self.client:
            response = self.client.get('/api/v2/charity')
            result = json.loads(response.data)
            self.assertEqual(
                'The requested resource could not be found on this server, check and try again', result['error'])
            self.assertEqual(response.status_code, 404)

    def test_405(self):
        with self.client:
            response = self.client.get(self.signupurl, data=json.dumps(self.register_data),
                                       content_type='application/json')

            result = json.loads(response.data)
            self.assertEqual(response.status_code, 405)
            self.assertEqual(
                'Method not allowed, ensure you enter the correct method and try again', result['error'])
