import unittest
from configs import config_handler 
# from client.client import Client
from configs.pwd_handler import generate_auth_file_with_encrypted_pwd

all_config =config_handler.get_configs_chains_from_yml('tests/testdata/test_general_configs.yml') # send a test yml file from testdata
private_key_filename = all_config.get('fernet_key_file')

tl_user = 'user1'
tl_pwd = 'user1'
tl_url  =  'localhost:5001'
# TLClient = Client(auth_config)


class TestConfigs(unittest.TestCase):
    
    
    def test_generate_auth_file_with_encrypted_pwd(self):
        generate_auth_file_with_encrypted_pwd('configs/secret.txt', private_key_filename,
                                          tl_user, tl_pwd, tl_url )
    
    def test_get_auth_configs(self):
        r =getconfig.get_auth_configs('tests/testdata/test_general_configs.yml') # send a test yml file from testdata
        #print(r)
        self.assertTrue(isinstance(r, dict))        
        self.assertTrue(k in r for k in ('password' ,'username', 'tokenleader_url'))
        
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
    
