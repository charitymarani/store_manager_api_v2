import json
from .base_tests import Testbase


class TestCart(Testbase):

    def test_add_cart(self):
        '''Only an attendant can add to cart'''
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
            # Add a product
            self.client.post(self.producturl, headers=dict(
                Authorization="Bearer " + token),
                data=json.dumps(self.productdata4),
                content_type='application/json')
            # Add to cart
            response_add_cart = self.client.post(self.carturl,
                                                 headers=dict(
                                                     Authorization="Bearer " + tokenatt),
                                                 data=json.dumps(
                                                     self.cart_data2),
                                                 content_type='application/json')
            result_add_cart = json.loads(response_add_cart.data)
            self.assertEqual("earphones added to cart",
                             result_add_cart["message"])
            self.assertEqual(response_add_cart.status_code, 201)
            # Test add non existent product
            response_add_no_product = self.client.post(self.carturl,
                                                       headers=dict(
                                                           Authorization="Bearer " + tokenatt),
                                                       data=json.dumps(
                                                           self.no_cart_item),
                                                       content_type='application/json')
            result_add_no_product = json.loads(response_add_no_product.data)
            self.assertEqual(
                "The item you want to add to cart does not exist", result_add_no_product["message"])
            # Test add same product to cart
            response_add_again = self.client.post(self.carturl,
                                                  headers=dict(
                                                      Authorization="Bearer " + tokenatt),
                                                  data=json.dumps(
                                                      self.cart_data2),
                                                  content_type='application/json')
            result_add_again = json.loads(response_add_again.data)
            self.assertEqual("earphones updated in cart",
                             result_add_again["message"])

    def test_get_all_cart(self):
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
            # Register attendant 2
            self.client.post(
                self.signupurl, headers=dict(Authorization="Bearer " + token),
                data=json.dumps(self.register_data3),
                content_type='application/json'
            )

            # Login attendant 2
            login_att2_response = self.client.post(
                self.loginurl,
                data=json.dumps(self.login_data3),
                content_type='application/json'
            )
            resultatt2 = json.loads(login_att2_response.data)
            tokenatt2 = resultatt2["token"]
            # Add a product
            self.client.post(self.producturl, headers=dict(
                Authorization="Bearer " + token),
                data=json.dumps(self.productdata4),
                content_type='application/json')
            # Add to cart
            self.client.post(self.carturl,
                            headers=dict(Authorization="Bearer " + tokenatt),
                            data=json.dumps(self.cart_data2),
                            content_type='application/json')
            # Get all cart
            response_get_cart = self.client.get(self.carturl,
                                                headers=dict(Authorization="Bearer " + tokenatt))
            self.assertEqual(response_get_cart.status_code, 200)
            #Get empty cart
            response_get_empty_cart = self.client.get(self.carturl,
                                                headers=dict(Authorization="Bearer " + tokenatt2))
            result_get_empty_cart=json.loads(response_get_empty_cart.data)

            self.assertEqual("The cart is currently empty",result_get_empty_cart["message"])

    
