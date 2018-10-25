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
            #Test successful post of a sale
            response = self.client.post(
                self.salesurl,headers=dict(Authorization="Bearer " + tokenatt),
                data=json.dumps(self.sales_data),
                content_type='application/json'
            )

            response_data = json.loads(response.data)
            print(response_data)
            self.assertEqual("A sale has been created successfully",response_data["response"]["message"])
            self.assertEqual(response.status_code, 201)
            #Test admin can't post a sale
            responsec = self.client.post(
                self.salesurl,headers=dict(Authorization="Bearer " + token),
                data=json.dumps(self.sales_data1),
                content_type='application/json'
            )

            response_datac = json.loads(responsec.data)
            self.assertEqual("Only an attendant is permitted to post sales",response_datac["message"])
            self.assertEqual(responsec.status_code, 401)
            #Test sale data can't be empty
            responsed = self.client.post(
                self.salesurl,headers=dict(Authorization="Bearer " + token),
                data=json.dumps(dict()
                ),
                content_type='application/json'
            )
            response_datad = json.loads(responsed.data)
            self.assertEqual("Fields cannot be empty",response_datad["message"])
            self.assertEqual(responsed.status_code, 400)
            #Test some missing fields
            responsee = self.client.post(
                self.salesurl,headers=dict(Authorization="Bearer " + token),
                data=json.dumps(dict(
                    items_count="",
                    total_amount=5000
                )),
                content_type='application/json'
            )

            response_datae = json.loads(responsee.data)
            self.assertEqual("Items_count and total_amount fields can't be empty",response_datae["message"])
            self.assertEqual(responsee.status_code, 206)


