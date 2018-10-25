import json
from .base_tests import Testbase


class TestProducts(Testbase):

    def test_post_product(self):
        '''Only an admin can post products'''
        with self.client:
            # login default admin
            login_response = self.client.post(
                self.loginurl,
                data=json.dumps(self.default_login),
                content_type='application/json'
            )
            result = json.loads(login_response.data)
            print(result)
            token = result["token"]
            # Register attendant
            self.client.post(
                self.signupurl, headers=dict(Authorization="Bearer " + token),
                data=json.dumps(self.register_data1),
                content_type='application/json'
            )

            # Login attendant
            login_att_response = self.client.post(
                self.loginurl,
                data=json.dumps(self.login_data1),
                content_type='application/json'
            )
            resultatt = json.loads(login_att_response.data)
            tokenatt = resultatt["token"]
            # Test successful post
            response = self.client.post(
                self.producturl, headers=dict(Authorization="Bearer " + token),
                data=json.dumps(self.productdata),
                content_type='application/json'
            )

            response_data = json.loads(response.data)
            print(response_data)
            self.assertEqual(
                "chunky heels, Posted!", response_data["response"]["message"])
            self.assertEqual(response.status_code, 201)
            # Test post product with existing product id
            responsez = self.client.post(
                self.producturl, headers=dict(Authorization="Bearer " + token),
                data=json.dumps(self.productdata),
                content_type='application/json'

            )

            response_dataz = json.loads(responsez.data)
            self.assertEqual(
                "The product Id you entered is being used for another product", response_dataz["response"]["message"])

            # Test empty data
            response1 = self.client.post(
                self.producturl, headers=dict(Authorization="Bearer " + token),
                data=json.dumps(dict()
                                ),
                content_type='application/json'

            )
            response_data1 = json.loads(response1.data)
            self.assertEqual("Fields cannot be empty",
                             response_data1["message"])
            self.assertEqual(response1.status_code, 400)
            # Test missing required fields
            response2 = self.client.post(
                self.producturl, headers=dict(Authorization="Bearer " + token),
                data=json.dumps(dict(
                    id="",
                    name="chunky",
                    category="shoes",
                    purchase_price=1000,
                    selling_price="",
                    quantity="",
                    low_limit="",
                    description="A wide based heel"

                )),
                content_type='application/json'

            )

            response_data2 = json.loads(response2.data)
            self.assertEqual("Some required fields are missing!",
                             response_data2["message"])
            self.assertEqual(response2.status_code, 206)
            # Test only admin can post products
            responseatt_post = self.client.post(
                self.producturl, headers=dict(
                    Authorization="Bearer " + tokenatt),
                data=json.dumps(self.productdata2),
                content_type='application/json'

            )

            response_data_att = json.loads(responseatt_post.data)
            self.assertEqual(
                "Only an admin is permitted to post products", response_data_att["message"])
            self.assertEqual(responseatt_post.status_code, 401)

    def test_get_all_products(self):
        with self.client:
            # login default admin
            login_response = self.client.post(
                self.loginurl,
                data=json.dumps(self.default_login),
                content_type='application/json'
            )
            result = json.loads(login_response.data)
        
            token = result["token"]
            #Get all products
            response = self.client.get(
                self.producturl, headers=dict(Authorization="Bearer " + token))
            self.assertEqual(response.status_code, 200)
