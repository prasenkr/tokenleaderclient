from cryptography.fernet import Fernet
import os
import configparser

           
def  get_fernet_cipher_from_keyfile(keyfilepath):
    if not  os.path.exists(keyfilepath):
        key = Fernet.generate_key()
        with open(keyfilepath, 'wb') as f:
            f.write(key)
    
    with open(keyfilepath, 'rb') as f:
       file_content = f.readline()        
       cipher_suite = Fernet(file_content)        
       return cipher_suite

          
def generate_auth_file_with_encrypted_pwd(confilepath, keyfilepath, tl_usr, tl_pwd, tl_url):  
    
    if not  os.path.exists(confilepath): 
        cipher_suite = get_fernet_cipher_from_keyfile(keyfilepath)
        byte_password = tl_pwd.encode("utf-8")
        encrypted_password = cipher_suite.encrypt(byte_password)
        encrypted_password_text = bytes(encrypted_password).decode("utf-8")                 
        config = configparser.ConfigParser()
        config['DEFAULT']['tl_user'] = tl_usr        
        config["DEFAULT"]['tl_url'] = tl_url
        config["DEFAULT"]['tl_password'] = encrypted_password_text 
        print ('creating file % s' % confilepath)
        with open(confilepath, 'w') as f:
            config.write(f)  
            msg =  ("file has been generated")
    else:
        msg = ("file already exists, delete this file first to generate a new one")
        
    print(msg)
    return msg
  

def get_txt_from_ini_n_decrypt(keyfilepath, confilepath, conf_section, conf_option): 
    #file_with_path = os.path.join(filepath, filename)    
    auto_encryption_status = (conf_section + '_' + conf_option + 
                             '_auto_encryption_status')
    config = configparser.ConfigParser()
    config.read(confilepath)
    if (config.has_option(conf_section, conf_option)) and \
      (config[conf_section][auto_encryption_status] == 'updated') :
          encrpted_text_from_file = config[conf_section][conf_option]
          byte_encrpted_text = encrpted_text_from_file.encode("utf-8")
          cipher_suite = get_fernet_cipher_from_keyfile(keyfilepath)
          byte_decrpted_text = cipher_suite.decrypt(byte_encrpted_text)
          clear_decrypted_text = bytes(byte_decrpted_text).decode("utf-8")
          print (clear_decrypted_text)          
          return clear_decrypted_text
    
    
             
    
'''
import os
os.chdir('/mnt/c/mydev/flask-tutorial/flaskr/encryption-learning/')secret_key_file_path = '/mnt/c/mydev/flask-tutorial/flaskr/encryption-learning/bhujaykey/info-ops-secret-key'
keyfile = '/mnt/c/mydev/flask-tutorial/flaskr/encryption-learning/bhujaykey/info-ops-secret-key'
config_file_path = '/mnt/c/mydev/flask-tutorial/flaskr/encryption-learning/mysettings.ini'
import  encrypt_with_fernet_key as efk
#efk.generate_secret_key_file(secret_key_file_name, secret_key_file_path)
#print (efk.get_fernet_cipher_from_keyfile(secret_key_file_name, secret_key_file_path))
#efk.encrypt_password_in_ini_file(config_file_name, config_file_path)
#efk.encrypt_txt_in_ini_file(config_file_name, config_file_path,'database', 'password')
efk.get_txt_from_ini_n_decrypt(keyfile, config_file_path,'database', 'password')


# #############Commom Code required for both encrypting password and decrypting it ##############
# '''
# key = Fernet.generate_key()
# '''
# print(key)
# key = 'b7i9cU3CobrW3dS3xbgoaQ79AgjAOAk0sfWhlLvQLMM='
# '''
# 
# cipher_suite = Fernet(key)
# 
# '''
# >>> print (cipher_suite)
# <cryptography.fernet.Fernet object at 0x7f637747f7f0>
# '''
# ##################################################################################################################
# '''
# ################# Code for encrypting password ####################################
# '''
# ciphered_text = cipher_suite.encrypt(b"SuperSecretPassword")   #required to be bytes
# 
# '''
# >>> print(ciphered_text)
# b'gAAAAABb5SZckONSDJdfB1ivRrssKGNsQQHliNV6di8SZD2oNJLsFL49lRAq0Y-QgOgi3X18xWGdsCYTC502hF7zvYakzC_NBOj4qSwasIkS49RtkTo1I_g='
# 
# write to a file in binary format
# '''
# with open('encrypted_pwd', 'wb') as f:
#     f.write(ciphered_text)   
# 
# ####################################################################################################
# '''
# #########################For decrypt  - need to have access to the key and create the cypher_suite
# '''
#        
# unciphered_text = (cipher_suite.decrypt(ciphered_text))
# 
# with open('encrypted_pwd', 'rb') as f:
#    for line in f:
#       pwd_from_file = line
# 
# unciper_pwd_from_file = cipher_suite.decrypt(pwd_from_file)
# 
# plain_text_unencryptedpassword = bytes(unciper_pwd_from_file).decode("utf-8") #convert to string
# 
# 
# '''
# >>> print(unciphered_text)
# b'SuperSecretPassword'
# 
# 
# >>> print (unciper_pwd_from_file)
# b'SuperSecretPassword'
# 
# 
# >>> print (plain_text_unencryptedpassword)
# SuperSecretPassword
# 
# '''

# def encrypt_password_in_ini_file(filename, filepath):
#     file_with_path = os.path.join(filepath, filename)
#     #print (file_with_path)
#     config = configparser.ConfigParser()
#     config.read(file_with_path)
#     clear_text_password = config['database']['password']
#     if (config.has_option('database','password')) and \
#         (not config.has_option('database', 'auto_encryption_status')) :        
#            clear_text_password = config['database']['password']
#            byte_password = clear_text_password.encode("utf-8")
#            #print (byte_password)
#            cipher_suite = get_fernet_cipher_from_keyfile(
#                secret_key_file_name, secret_key_file_path)
#            encrypted_password = cipher_suite.encrypt(byte_password)
#            encrypted_password_text = bytes(encrypted_password).decode("utf-8")
#            print (encrypted_password_text)
#            config['database']['password'] = encrypted_password_text
#            config['database']['auto_encryption_status'] = 'updated'
#            with open(file_with_path, 'w') as f:
#                config.write(f)  




