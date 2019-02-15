import yaml
import os
from cryptography.fernet import Fernet
import configparser
import six


class Configs():
    
    tl_user = ''
    tl_password = ''
    tl_url = ''
        
    def __init__(self, config_file='/etc/tlclient/general_configs.yml'):
#         if self.general_config['user_auth_info_from'] == 'file': 
        if not os.path.exists(config_file):
            print("you need to use tlconfig command to create a config file "
                  "first in {} , if the file is in other location give the "
                  "filename with path as parameter to Config or Client "
                  "initialization".format(config_file))
        self.config_file = config_file
        self.general_config = self.parse_yml(self.config_file)
        self.fernet_key_file =  os.path.expanduser(
            self.general_config['fernet_key_file'])
        self.user_auth_info_file_location = os.path.expanduser(
            self.general_config['user_auth_info_file_location']) 
        with open(os.path.expanduser('~/.ssh/id_rsa.pub'), 'r') as f:
                self.public_key = f.read() 
        if self.general_config['tl_public_key']:
            self.tl_public_key = self.general_config['tl_public_key']
        else:
            self.tl_public_key =  self.public_key
                    
                    
    def parse_yml(self, file):
        with open(file, 'r') as f:
            try:
                parsed = yaml.safe_load(f)
            except yaml.YAMLError as e:            
                raise ValueError(six.text_type(e))
            return parsed or {}
        
    
    def generate_user_auth_file(self, tl_usr, tl_pwd, tl_url):
        '''
        Also stores encrypted password. user should use a cli utility to call this method to generate 
        the file
        '''
        filepath =  os.path.expanduser(self.user_auth_info_file_location)
        dirpath = os.path.dirname(filepath)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)            
        if not  os.path.exists(filepath): 
            cipher_suite = self.get_fernet_cipher_from_keyfile(self.fernet_key_file)
            byte_password = tl_pwd.encode("utf-8")
            encrypted_password = cipher_suite.encrypt(byte_password)
            encrypted_password_text = bytes(encrypted_password).decode("utf-8")                 
            config = configparser.ConfigParser()
            config['DEFAULT']['tl_user'] = tl_usr        
            config["DEFAULT"]['tl_url'] = tl_url
            config["DEFAULT"]['tl_password'] = encrypted_password_text 
            print ('creating file % s' % self.user_auth_info_file_location)
            with open(filepath, 'w') as f:
                config.write(f)  
                msg =  ("file {} has been generated".format(filepath))
        else:
            msg = ("file {} already exists, delete this file first to generate a new one".format(filepath))
            
        print(msg)
        return self
        
    
    def  get_fernet_cipher_from_keyfile(self, keyfilepath):
        filepath =  os.path.expanduser(keyfilepath)
        dirpath = os.path.dirname(filepath)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)        
        if not  os.path.exists(keyfilepath):
            key = Fernet.generate_key()
            with open(filepath, 'wb') as f:
                f.write(key)
        
        with open(filepath, 'rb') as f:
           file_content = f.readline()        
           cipher_suite = Fernet(file_content)        
           return cipher_suite
       
    def get_user_auth_info(self):         
        config = configparser.ConfigParser()
        filepath =  os.path.expanduser(self.user_auth_info_file_location)
        #print(filepath)
        try:            
            config.read(filepath)            
            self.tl_user = config['DEFAULT']['tl_user']           
            self.tl_url = config["DEFAULT"]['tl_url']
            encrpted_text_from_file = config["DEFAULT"]['tl_password']                  
            msg = "got all info from file and decrypted the password"
        except Exception as e:
            msg = " auth file or relevant section is not found, the full error is {}".format(e)
            print(msg)
        byte_encrpted_text = encrpted_text_from_file.encode("utf-8")
        cipher_suite = self.get_fernet_cipher_from_keyfile(self.fernet_key_file)
        byte_decrpted_text = cipher_suite.decrypt(byte_encrpted_text)
        clear_decrypted_text = bytes(byte_decrpted_text).decode("utf-8")
        self.tl_password = clear_decrypted_text
        return self
    
    
    

#     
