import unittest
# from flask import Flask
from flask_testing import TestCase
import json
from  tokenleaderclient import flaskapp
from tokenleaderclient.rbac import enforcer
from tokenleaderclient.flaskapp.APIroutes.firstapi import bp1

bp_list = [bp1]

app = flaskapp.create_app(blue_print_list=bp_list)

role_acl_map_file='tokenleaderclient/tests/testdata/role_to_acl_map.yml'

class BaseTestCase(TestCase):
    def create_app(self):       
        return app     
    
    def test_get_token(self):
        response = enforcer.get_token()
        self.assertTrue(isinstance(response, str))                              
#         data = json.loads(response.decode())
#         print(data)
#         self.assertTrue(data['status'] == 'success')
#         self.assertTrue('auth_token' in data)
#     
    def test_verify_token(self):
        token = enforcer.get_token()
        result = enforcer.verify_token(token)
        self.assertTrue(isinstance(result, dict))
    
    def test_ep3(self):
        token = enforcer.get_token()
#         print(response)
        self.assertTrue(isinstance(token, str))         
        with self.client:
            self.headers = {"X-Auth-Token": token}
            response = self.client.get('/ep3', headers=self.headers)
            #print(response.data.decode())            
            #return_data = json.loads(response)
            return_data = json.loads(response.data.decode())
            #print(return_data)
            self.assertTrue(return_data['message'] == 'Catch me if you can')
            print('ep2 tested ok')

    def test_ep3_failed_authetication(self):
        token = enforcer.get_token()
#         print(response)
        self.assertTrue(isinstance(token, str))         
        with self.client:
            self.headers = {"X-Auth-Token": token}
            response = self.client.get('/ep3', headers=self.headers)
#             print(response.data.decode())            
            #return_data = json.loads(response)
            return_data = json.loads(response.data.decode())
            #print(return_data['message'])
            self.assertTrue(return_data['message'] == \
                            'this endpoint is restricted , authenticaton or authorization failed')
            print('ep2 tested ok with authntication failure scnerio')
            

# if __name__ =='__main__':
#     unittest.main()
    
