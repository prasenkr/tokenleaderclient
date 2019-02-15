import requests
import json
import jwt

from tokenleaderclient.configs.config_handler import Configs


class Client():   
     
    def __init__(self , conf_file=None):
        if  conf_file:
            self.conf =Configs(conf_file)
        else:
            self.conf =Configs() 
        self.ssl_verify = self.conf.ssl_verify    
        self.auth_config = self.conf.get_user_auth_info()
        self.tl_username = self.auth_config.tl_user
        self.tl_password = self.auth_config.tl_password
        self.tl_url = self.auth_config.tl_url
        self.tokenleader_public_key = self.auth_config.tl_public_key
        self.ssl_verify = self.conf.ssl_verify
        

    def get_token(self):
        api_route = '/token/gettoken'
        service_endpoint = self.tl_url + api_route
        headers={'content-type':'application/json'}
        self.data=json.dumps(dict(username=self.tl_username, password=self.tl_password))
        r = requests.post(service_endpoint, self.data, headers=headers, verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        #print(r_dict)
        return r_dict 
              
    
    def verify_token_from_tl(self,token,):
        api_route = '/token/verify_token'
        service_endpoint = self.tl_url + api_route
        headers={'X-Auth-Token': token}    
        r = requests.get(service_endpoint, headers=headers, verify=self.ssl_verify)   
    #     print(r.content)
    #     print(type(r.content))
        r_dict = json.loads(r.content.decode())  
        return r_dict
    
        
    def verify_token(self, token): 
        #print(self.tokenleader_public_key)  
        payload = self._decrypt_n_verify_token(token, self.tokenleader_public_key)    
        if payload == "Signature expired. Please log in again." :
            status = "Signature expired"
            message = "Signature expired. Please log in and get a fresh token and send it for reverify."
        elif payload == "Invalid token. Please log in again.":
            status = "Invalid token"
            message = "Invalid token. obtain a valid token and send it for verifiaction"
        else:
            status = "Verification Successful"
            message = "Token has been successfully decrypted"   
            
        responseObject = {
                            'status': status,
                            'message': message,
                            'payload': payload}
#         print(responseObject)      
        return responseObject
    
    
    def _decrypt_n_verify_token(self, auth_token, pub_key):
        try:
            payload = jwt.decode(
                auth_token,
                pub_key,
                algorithm=['RS512']
            )
            
            return payload
    #         
        except jwt.ExpiredSignatureError:
                return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
                return 'Invalid token. Please log in again.'
            
    def list_users(self):
        token = self.get_token().get('auth_token')
        api_route = '/list/users'
        service_endpoint = self.tl_url + api_route
        headers={'X-Auth-Token': token}    
        r = requests.get(service_endpoint, headers=headers, verify=self.ssl_verify)       #     
        r_dict = json.loads(r.content.decode())
#         print(r_dict)  # for displaying from the cli  print in cli parser
        return r_dict
        
    
