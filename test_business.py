import unittest
import json
import os
from app import app

class TestBusinessApiResponse(unittest.TestCase):

    def setUp(self):
        self.test = app.test_client()

    def register_user_helper(self,email='unique@unique',password='u#n~q'):
        credentials = {
            'email':email,
            'password':password
            }
        return self.test.post('/weConnect/api/v1/registeruser',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(credentials)
               )

    def login_helper(self,email='unique@unique',password='u#n~q'):
        credentials = {
            'email':email,
            'password':password
            }
        return self.test.post('/weConnect/api/v1/login',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(credentials)
               )
    def register_business_helper(self,businessname='wishywashy',businesscategory='laundry',businesslocation='trm'):
        self.register_user_helper()
        login_res = self.login_helper()
        loggeduserid = json.loads(login_res.data.decode())['userid']
        businessdata = {
                    'userid':loggeduserid,
                    'businessname':businessname,
                    'businesscategory':businesscategory,
                    'businesslocation':businesslocation
                }
        return self.test.post('/weConnect/api/v1/businesses',
                headers={'Content-Type': 'application/json',
                        'Authorization':'Bearer' + 'loggeduserid'},
                data=json.dumps(businessdata)
               )

    def test_can_register_business_successfully(self):
        business_res = self.register_business_helper()
        business_result = json.loads(business_res.data.decode())
        self.assertEqual(business_result['message'],'business created successfully')
        self.assertEqual(business_res.status_code, 201)

    def test_can_get_all_businesses(self):
        self.register_business_helper()
        res = self.test.get('/weConnect/api/v1/businesses')
        result = json.loads(res.data.decode())['Business']
        self.assertTrue(result)

    def test_can_get_business_by_id(self):
        register_res = self.register_business_helper(businessname = 'midventures',
            businesscategory = 'wholesalers',
            businesslocation = 'Haile sellasie'
            )
        res = self.test.get('/weConnect/api/v1/businesses/1')
        result = json.loads(res.data.decode())['Business']
        self.assertTrue(result)
        self.assertEqual('midventures', BUSINESS[0]['name'])
        self.assertEqual('wholesalers', BUSINESS[0]['category'])
        self.assertEqual('Haile sellasie', BUSINESS[0]['location'])

    def test_owner_can_update_business(self):
        self.register_business_helper()
        editcredentials = {
                    'businessname':'wizshine',
                    'businesscategory':'house cleaning',
                    'businesslocation':'moi avenue'
                }
        res = self.test.post('/weConnect/api/v1/businesses/1',
                headers={'Content-Type': 'application/json'},
                data = json.dumps(editcredentials)
                )
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],'successfully updated business')
        self.assertEqual(res.status_code, 200)

    def test_owner_can_delete_business(self):
        self.register_business_helper()
        res = self.test.delete('/weConnect/api/v1/businesses/1')
        self.assertEqual(res.status_code, 200)


if __name__=='__main__':
    unittest.main()
