import json
from .base_tests import Testbase


class TestSales(Testbase):

    def test_post_sales(self):
        '''Only an attendant can post sales'''
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
                data=json.dumps(self.productdata),
                content_type='application/json')
            # Add to cart
            response_add_cart = self.client.post(self.carturl,
                headers=dict(Authorization="Bearer " + tokenatt),
                data=json.dumps(self.cart_data),
                content_type='application/json')
            result_add_cart=json.loads(response_add_cart.data)
            self.assertEqual("scarf added to cart",result_add_cart["message"])
            self.assertEqual(response_add_cart.status_code,201)

            # Test successful post of a sale
            response=self.client.post(
                self.salesurl, headers = dict(
                    Authorization="Bearer " + tokenatt),
                content_type = 'application/json'
            )

            response_data=json.loads(response.data)
            self.assertEqual("A sale has been created successfully",
                             response_data["message"])
            self.assertEqual(response.status_code, 201)
            # Test admin can't post a sale
            responsec=self.client.post(
                self.salesurl, headers=dict(Authorization="Bearer " + token),
                content_type='application/json'
            )

            response_datac = json.loads(responsec.data)
            self.assertEqual(
                "Only an attendant is permitted to post sales", response_datac["message"])
            self.assertEqual(responsec.status_code, 401)
            # Test sale data can't be empty
            responsee = self.client.post(
                self.salesurl, headers=dict(
                    Authorization="Bearer " + tokenatt2),
                content_type='application/json'
            )
            response_datae = json.loads(responsee.data)
            self.assertEqual(
                "The cart is currently empty,add items to cart to make a sale", response_datae["message"])

    def test_get_all_sales(self):
        '''Only an admin can view all sales records'''
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
                data=json.dumps(self.productdata),
                content_type='application/json')
            # Add to cart
            self.client.post(self.carturl,
                headers=dict(Authorization="Bearer " + tokenatt),
                data=json.dumps(self.cart_data),
                content_type='application/json')

            # Let attendant post of a sale
            self.client.post(
                self.salesurl, headers = dict(
                    Authorization="Bearer " + tokenatt),
                content_type = 'application/json'
            )
            # Let admin get all sales
            response = self.client.get(
                self.salesurl, headers=dict(Authorization="Bearer " + token))
            self.assertEqual(response.status_code, 200)
            # Test attendant is not allowed to view all sales
            responseb = self.client.get(self.salesurl, headers=dict(
                Authorization="Bearer " + tokenatt))
            responseb_data = json.loads(responseb.data)
            self.assertEqual(
                "Only an admin can view all sales records", responseb_data["message"])
            self.assertEqual(responseb.status_code, 401)

    def test_get_sale_by_id(self):
        with self.client:
            # login defailtadmin and register two attendants
            login_response = self.client.post(
                self.loginurl,
                data=json.dumps(self.default_login),
                content_type='application/json'
            )
            result = json.loads(login_response.data)

            token = result["token"]
            # Register attendant1
            self.client.post(
                self.signupurl, headers=dict(Authorization="Bearer " + token),
                data=json.dumps(self.register_data2),
                content_type='application/json'
            )

            # Login attendant1
            login_att_response = self.client.post(
                self.loginurl,
                data=json.dumps(self.login_data2),
                content_type='application/json'
            )
            resultatt = json.loads(login_att_response.data)
            tokenatt = resultatt["token"]
            # Register attendant2
            self.client.post(
                self.signupurl, headers=dict(Authorization="Bearer " + token),
                data=json.dumps(self.register_data),
                content_type='application/json'
            )

            # Login attendant2
            login_att_response2 = self.client.post(
                self.loginurl,
                data=json.dumps(self.login_data),
                content_type='application/json'
            )
            resultatt2 = json.loads(login_att_response2.data)
            tokenatt2 = resultatt2["token"]
            # Add a product
            self.client.post(self.producturl, headers=dict(
                Authorization="Bearer " + token),
                data=json.dumps(self.productdata),
                content_type='application/json')
            # Add to cart
            self.client.post(self.carturl,
                headers=dict(Authorization="Bearer " + tokenatt),
                data=json.dumps(self.cart_data),
                content_type='application/json')

            # Let attendant1 post of a sale
            self.client.post(
                self.salesurl, headers = dict(
                    Authorization="Bearer " + tokenatt),
                content_type = 'application/json'
            )

            # let the attendant who posted get the sale
            responseatt = self.client.get(
                self.salesurl+'/1', headers=dict(Authorization="Bearer " + tokenatt))

            self.assertEqual(responseatt.status_code, 200)
            # let the admin  get the sale
            responseadmin = self.client.get(
                self.salesurl+'/1', headers=dict(Authorization="Bearer " + token))
            self.assertEqual(responseadmin.status_code, 200)
            # Test another attendant can't get a sale they didn't post
            responseatt2 = self.client.get(
                self.salesurl+'/1', headers=dict(Authorization="Bearer " + tokenatt2))
            resultatt2 = json.loads(responseatt2.data)
            self.assertEqual(
                "Only an admin or attendant who created this sale are allowed to view it", resultatt2["message"])
            self.assertEqual(responseatt2.status_code, 401)
