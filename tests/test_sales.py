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
            # Test successful post of a sale
            response = self.client.post(
                self.salesurl, headers=dict(
                    Authorization="Bearer " + tokenatt),
                data=json.dumps(self.sales_data),
                content_type='application/json'
            )

            response_data = json.loads(response.data)
            print(response_data)
            self.assertEqual("A sale has been created successfully",
                             response_data["response"]["message"])
            self.assertEqual(response.status_code, 201)
            # Test admin can't post a sale
            responsec = self.client.post(
                self.salesurl, headers=dict(Authorization="Bearer " + token),
                data=json.dumps(self.sales_data1),
                content_type='application/json'
            )

            response_datac = json.loads(responsec.data)
            self.assertEqual(
                "Only an attendant is permitted to post sales", response_datac["message"])
            self.assertEqual(responsec.status_code, 401)
            # Test sale data can't be empty
            responsed = self.client.post(
                self.salesurl, headers=dict(Authorization="Bearer " + token),
                data=json.dumps(dict()
                                ),
                content_type='application/json'
            )
            response_datad = json.loads(responsed.data)
            self.assertEqual("Fields cannot be empty",
                             response_datad["message"])
            self.assertEqual(responsed.status_code, 400)
            # Test some missing fields
            responsee = self.client.post(
                self.salesurl, headers=dict(Authorization="Bearer " + token),
                data=json.dumps(dict(
                    items_count="",
                    total_amount=5000
                )),
                content_type='application/json'
            )

            response_datae = json.loads(responsee.data)
            self.assertEqual(
                "Items_count and total_amount fields can't be empty", response_datae["message"])
            self.assertEqual(responsee.status_code, 206)

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

            # let attendant post a sale
            self.client.post(
                self.salesurl, headers=dict(
                    Authorization="Bearer " + tokenatt),
                data=json.dumps(self.sales_data1),
                content_type='application/json'
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
            # login default admin
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

            # let attendant1 post a sale
            self.client.post('/api/v1/sales',
                             headers=dict(Authorization="Bearer " + tokenatt),
                             data=json.dumps(self.sales_data),
                             content_type='application/json'
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
           
