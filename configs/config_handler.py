import yaml
import os
from cryptography.fernet import Fernet
import configparser


class Configs():
    
    tl_user = ''
    tl_password = ''
    tl_url = ''
    
    def __init__(self, config_file):
        self.config_file = config_file
        self.general_config = self.parse_yml(self.config_file)
        self.fernet_key_file =  self.general_config['fernet_key_file']
        self.user_auth_info_file_location = self.general_config['user_auth_info_file_location'] 
        if self.general_config['user_auth_info_from'] == 'file':
            if self.general_config.get('private_key_file_location') == 'default':
                self.private_key_filename = os.path.expanduser('~/.ssh/id_rsa')
            else:
                self.private_key_filename = self.general_config.get('private_key_file_location')
                
            if self.general_config.get('public_key_file_location') == 'default':
                self.public_key_filename = os.path.expanduser('~/.ssh/id_rsa.pub')
            else:
                self.public_key_filename = self.general_config.get('public_key_file_location')
            
            with open(self.private_key_filename, 'r') as f:
                self.private_key = f.read()
            with open(self.public_key_filename, 'r') as f:
                    self.public_key = f.read()   
                    
                    
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
        if not  os.path.exists(self.user_auth_info_file_location): 
            cipher_suite = self.get_fernet_cipher_from_keyfile(self.fernet_key_file)
            byte_password = tl_pwd.encode("utf-8")
            encrypted_password = cipher_suite.encrypt(byte_password)
            encrypted_password_text = bytes(encrypted_password).decode("utf-8")                 
            config = configparser.ConfigParser()
            config['DEFAULT']['tl_user'] = tl_usr        
            config["DEFAULT"]['tl_url'] = tl_url
            config["DEFAULT"]['tl_password'] = encrypted_password_text 
            print ('creating file % s' % self.user_auth_info_file_location)
            with open(self.user_auth_info_file_location, 'w') as f:
                config.write(f)  
                msg =  ("file has been generated")
        else:
            msg = ("file already exists, delete this file first to generate a new one")
            
        print(msg)
        return self
        
    
    def  get_fernet_cipher_from_keyfile(self, keyfilepath):        
        if not  os.path.exists(keyfilepath):
            key = Fernet.generate_key()
            with open(keyfilepath, 'wb') as f:
                f.write(key)
        
        with open(keyfilepath, 'rb') as f:
           file_content = f.readline()        
           cipher_suite = Fernet(file_content)        
           return cipher_suite
       
    def get_user_auth_info(self):         
        config = configparser.ConfigParser()
        try:            
            config.read(self.user_auth_info_file_location)            
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
