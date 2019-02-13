import flask
from flask import request, make_response
import requests
import json
import functools

from tokenleaderclient.rbac.policy import load_service_access_policy 
from tokenleaderclient.rbac.policy import load_role_to_acl_map
from tokenleaderclient.rbac.wfc import WorkFuncContext
from  tokenleaderclient.client.client import Client 

role_acl_map_file_prod_settings='tokenleaderclient/acl/role_to_acl_map.yml'
WFC = WorkFuncContext()
tl_client = Client()


def get_token():
    r_dict = tl_client.get_token()            
    if r_dict['status'] == 'success': 
        token_received = r_dict['auth_token'] 
#         print('got the token as : {}'.format(token_received))
    else:
          token_received = r_dict['status']
    return token_received   # we need to handle auth faliure 


def verify_token(token):
    r_dict = tl_client.verify_token(token)
    return r_dict


def extract_token_data_from_api_request(verifed_token=None):
    
    token_verification_result = {}
    
    if not verifed_token: 
        auth_token = flask.request.headers.get('X-Auth-Token')
        if not auth_token :
            #flask.abort(404)
            return ("This end point need authentication, 'X-Auth-Token' key \n \
                              is not present in the  request header \n")
        else:
            #auth_token = fdata['auth_token']
            token_verification_result = verify_token(auth_token) 
    else:
        if isinstance(verifed_token, dict):
            token_verification_result =   verifed_token
        else: 
            token_verification_result['message']  = 'invalid token type' 
          
    return  token_verification_result    
   

def compare_role_in_token_with_acl_map(user_role_in_token, rule_name, 
                                       role_acl_map_file=role_acl_map_file_prod_settings):
    role_to_acl_map_list = load_role_to_acl_map(role_acl_map_file)
#     print(role_to_acl_map_list)
    found_role_acl_map = []
    for role_acl_map in role_to_acl_map_list:        
        if  (role_acl_map.get('name') == user_role_in_token
             and rule_name in role_acl_map.get('allow') ):            
            found_role_acl_map.append(True)
        else:
            found_role_acl_map.append(False)    
#     print(found_role_acl_map)           
    if  True in found_role_acl_map :                                                    
        print('authorization success for rule: {}, role: {}'.format(
            user_role_in_token, rule_name))
        return True
    else:
        msg = ('role:  {} does not have permission for rule:  {}'.format(
                    user_role_in_token, rule_name)) 
        print(msg)
#         print(role_to_acl_map_list)
        return False   
    
    
def extract_roles_from_verified_token_n_compare_acl_map(rule_name, role_acl_map_file, verified_token=None):
    token_verification_result = extract_token_data_from_api_request(verified_token)
    #print(token_verification_result)
    if token_verification_result['status'] == 'Verification Successful' :                   
        #username = token_verification_result['payload'].get('sub').get('username')
        wcf_from_token = token_verification_result['payload'].get('sub').get('wfc')
        roles_in_token = token_verification_result['payload'].get('sub').get('roles')
        print("user has following roles: {}".format(roles_in_token))
        status_list_of_rule_check = []
        for user_role_in_token in roles_in_token:
            # don't compare  roles in yml file  when the role name from token is admin
            if user_role_in_token == 'admin':
                  status_list_of_rule_check.append(True)
            else:      
                compare_status = compare_role_in_token_with_acl_map(user_role_in_token, 
                                                   rule_name,
                                                   role_acl_map_file)
                #print(compare_status)            
                status_list_of_rule_check.append(compare_status)            
        #print(status_list_of_rule_check)    
        if True in status_list_of_rule_check:
            return True, wcf_from_token, token_verification_result['message']
        else:
            return False, wcf_from_token, token_verification_result['message']  
    else:
        return False, False, token_verification_result['message'] 
            


def enforce_access_rule_with_token(rule_name, role_acl_map_file=role_acl_map_file_prod_settings,
                                    verified_token=None,):
    def decorator(f):  
        @functools.wraps(f)
        def wrapper_function(*args, **kws):
            role_exists_in_acl, wcf_from_token, msg = \
            extract_roles_from_verified_token_n_compare_acl_map(rule_name, role_acl_map_file,
                                                                   verified_token)
            #print(role_exists_in_acl, wcf_from_token)
            if wcf_from_token:
                WFC.setcontext(wcf_from_token)
                #print(WFC.org)
                kws['wfc'] = WFC
            if role_exists_in_acl:
                
                    return f(*args, **kws)
            else:
                msg = "this endpoint is restricted , authenticaton or authorization failed" 
                print(msg)
                return json.dumps({'message': msg})
                            
        return wrapper_function
    return decorator















def validate_request(f):
  @functools.wraps(f)
  def decorated_function(*args, **kws):    
        fdata = flask.request.get_json()
        if (not fdata) or ('auth_token' not in fdata) :
            #flask.abort(404)
            return ("This end point need authentication, 'auth_token' key \n \
                  is not present in the  request data \n")
        else:
            auth_token = fdata['auth_token']
            token_verification_result = verify_token(auth_token, auth_url)        
            if token_verification_result['status'] == 'Verification Successful' :                   
                username = token_verification_result['payload'].get('sub').get('username') 
                role = token_verification_result['payload'].get('sub').get('role')
                if role != 'abc':
                    #do more stuff
                    return f(*args, **kws)
                #handle else for authentication errors
            #handle {'message': 'Token has been successfully decrypted', 'payload': 'Signature expired. Please log in again.', 'status': 'Verification Successful'}
            else:
                return token_verification_result['message']    
  return decorated_function



