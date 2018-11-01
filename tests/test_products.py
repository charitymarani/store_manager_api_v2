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
            self.assertEqual(
                "scarf, Posted!", response_data["message"])
            self.assertEqual(response.status_code, 201)
            # Test post product with existing product id
            responsez = self.client.post(
                self.producturl, headers=dict(Authorization="Bearer " + token),
                data=json.dumps(self.productdata),
                content_type='application/json'

            )

            response_dataz = json.loads(responsez.data)
            self.assertEqual(
                "The product already exists,you can update product quantity instead", response_dataz["message"])

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
                data=json.dumps(self.productdata),
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
            # Get all products
            response = self.client.get(
                self.producturl, headers=dict(Authorization="Bearer " + token))
            self.assertEqual(response.status_code, 200)

    def test_get_product_by_id(self):
        with self.client:
            # login default admin
            login_response = self.client.post(
                self.loginurl,
                data=json.dumps(self.default_login),
                content_type='application/json'
            )
            result = json.loads(login_response.data)

            token = result["token"]

            # Test successful get product by id
            response = self.client.get(
                self.producturl+'/140', headers=dict(Authorization="Bearer " + token))
            self.assertEqual(response.status_code, 200)
            # Test get product that doesn't exist
            response1 = self.client.get(
                self.producturl+'/700', headers=dict(Authorization="Bearer " + token))
            resp = json.loads(response1.data)
            self.assertEqual(
                "product_code does not exist in our records", resp["message"])

    def test_edit_product(self):
        with self.client:
            # login default admin
            login_response = self.client.post(
                self.loginurl,
                data=json.dumps(self.default_login),
                content_type='application/json'
            )
            result = json.loads(login_response.data)

            token = result["token"]
            # Post a product
            self.client.post(
                self.producturl, headers=dict(Authorization="Bearer " + token),
                data=json.dumps(self.productdata3),
                content_type='application/json'
            )

            # Test successful edit
            response = self.client.put(
                self.producturl+'/140', data=json.dumps(self.edit_data),
                headers=dict(Authorization="Bearer " + token),
                content_type='application/json'
            )
            response_data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual("Product updated successfully!",
                             response_data["message"])
            # Test empty data
            response1 = self.client.put(
                self.producturl+'/140', data=json.dumps({}),
                headers=dict(Authorization="Bearer " + token),
                content_type='application/json'
            )
            response_data1 = json.loads(response1.data)
            self.assertEqual("Fields cannot be empty",
                             response_data1["message"])
            self.assertEqual(response1.status_code, 400)
            # Test all fields missing
            response2 = self.client.put(
                self.producturl+'/140', data=json.dumps(self.empty_data_fields),
                headers=dict(Authorization="Bearer " + token),
                content_type='application/json'
            )
            response_data2 = json.loads(response2.data)
            self.assertEqual(
                "All fields cannot be empty enter data to edit", response_data2["message"])
            self.assertEqual(response2.status_code, 400)
            # Test nonexistent product
            response3 = self.client.put(
                self.producturl+'/554', data=json.dumps(self.edit_data),
                headers=dict(Authorization="Bearer " + token),
                content_type='application/json'
            )
            response_data3 = json.loads(response3.data)
            self.assertEqual("Product does not exist",
                             response_data3["message"])
            # Register attendant
            self.client.post(
                self.signupurl, headers=dict(Authorization="Bearer " + token),
                data=json.dumps(self.register_data2),
                content_type='application/json'
            )

            # Login attendant
            login_att_response = self.client.post(
                self.loginurl,
                data=json.dumps(self.login_data2),
                content_type='application/json'
            )
            resultatt = json.loads(login_att_response.data)
            tokenatt = resultatt["token"]
            # Test attendant cannot edit product
            response4 = self.client.put(
                self.producturl+'/140', data=json.dumps(self.edit_data),
                headers=dict(Authorization="Bearer " + tokenatt),
                content_type='application/json'
            )
            response_data4 = json.loads(response4.data)
            self.assertEqual("Only admin can edit a product",
                             response_data4["message"])
            self.assertEqual(response4.status_code, 401)

    def test_delete_product(self):
        with self.client:
            # login default admin
            login_response = self.client.post(
                self.loginurl,
                data=json.dumps(self.default_login),
                content_type='application/json'
            )
            result = json.loads(login_response.data)
            token = result["token"]
            # Post a product
            self.client.post(
                self.producturl, headers=dict(Authorization="Bearer " + token),
                data=json.dumps(self.productdata3),
                content_type='application/json'
            )
            # Test successfull delete
            response = self.client.delete(
                self.producturl+'/140', headers=dict(Authorization="Bearer " + token))
            result = json.loads(response.data)
            self.assertEqual("product has been deleted!",
                             result["message"])
            self.assertEqual(response.status_code, 200)
            # Test nonexistent product
            response2 = self.client.delete(
                self.producturl+'/700', headers=dict(Authorization="Bearer " + token))
            result2 = json.loads(response2.data)
            self.assertEqual(
                "product_code does not exist in our records", result2["message"])
            # Test attendant cannot delete product
            # Register attendant
            self.client.post(
                self.signupurl, headers=dict(Authorization="Bearer " + token),
                data=json.dumps(self.register_data3),
                content_type='application/json'
            )

            # Login attendant
            login_att_response = self.client.post(
                self.loginurl,
                data=json.dumps(self.login_data3),
                content_type='application/json'
            )
            resultatt = json.loads(login_att_response.data)
            tokenatt = resultatt["token"]

            response3 = self.client.delete(
                self.producturl+'/504', headers=dict(Authorization="Bearer " + tokenatt))
            result3 = json.loads(response3.data)
            self.assertEqual("Only admin can delete a product",
                             result3["message"])
            self.assertEqual(response3.status_code, 401)
