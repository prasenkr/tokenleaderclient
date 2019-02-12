import os
import unittest
from configs.config_handler import Configs
from client.client import Client

settings_file = 'tests/testdata/test_general_configs.yml'
tl_user = 'user1'
tl_pwd = 'user1'
tl_url  =  'http://localhost:5001'
TLClient = Client(settings_file)     


class TestConfigs(unittest.TestCase):
    
    def test_generate_auth_file_with_encrypted_pwd(self):
        conf.generate_user_auth_file(tl_user, tl_pwd, tl_url )
        self.assertTrue(os.path.exists('tests/testdata/test_general_configs.yml'))
        
    def test_get_user_auth_info(self):
        conf.get_user_auth_info()
        self.assertTrue((conf.tl_password , conf.tl_user, conf.tl_url) == (tl_pwd, tl_user, tl_url))
    
         
    def test_get_token_method(self):           
        r1 = TLClient.get_token()
        self.assertTrue(isinstance(r1, dict))        
        self.assertTrue(k in r for k in ('auth_token' ,'service_catalog', 'status'))   
    
        
    def test_verify_token_from_tl(self):
        r = TLClient.get_token()
        token = r['auth_token']
        r1  = TLClient.verify_token_from_tl(token)
        self.assertTrue(r1['status'] == 'Verification Successful')        
        self.assertTrue(isinstance(r1.get('payload').get('sub'), dict))
        
    
    def test_verify_token_local(self):
        r = TLClient.get_token()
        token = r['auth_token']
        r1 = TLClient.verify_token(token)
        self.assertTrue(r1['status'] == 'Verification Successful')        
        self.assertTrue(isinstance(r1.get('payload').get('sub'), dict))
    
