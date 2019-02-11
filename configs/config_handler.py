import yaml
import os


def parse_yml(file):
    with open(file, 'r') as f:
        try:
            parsed = yaml.safe_load(f)
        except yaml.YAMLError as e:            
            raise ValueError(six.text_type(e))
        return parsed or {}

def get_configs_chains_from_yml(file='configs/general_configs.yml'):
    general_config = parse_yml(file)
    if general_config['user_auth_info_from'] == 'file':
        if general_config.get('private_key_file_location') == 'default':
            private_key_filename = os.path.expanduser('~/.ssh/id_rsa')
        else:
            private_key_filename = general_config.get('private_key_file_location')
            
        if general_config.get('public_key_file_location') == 'default':
            public_key_filename = os.path.expanduser('~/.ssh/id_rsa.pub')
        else:
            public_key_filename = general_config.get('public_key_file_location')
        
        with open(private_key_filename, 'r') as f:
            private_key = f.read()
        with open(public_key_filename, 'r') as f:
                public_key = f.read()  
                
    return {"public_key_filename": public_key_filename,
            "private_key_filename": private_key_filename,
            "private_key": private_key,
            "public_key": public_key,
            "fernet_key_file": general_config['fernet_key_file'] }

# general_config = get_general_configs_from_yml()

# if general_config['user_auth_info_from'] == 'file':
#     if general_config.get('private_key_file_location') == 'default':
#         private_key_filename = os.path.expanduser('~/.ssh/id_rsa')
#     else:
#         private_key_filename = general_config.get('private_key_file_location')
#         
#     if general_config.get('public_key_file_location') == 'default':
#         public_key_filename = os.path.expanduser('~/.ssh/id_rsa.pub')
#     else:
#         public_key_filename = general_config.get('public_key_file_location')
#     
#     with open(private_key_filename, 'r') as f:
#             private_key = f.read()
#     with open(public_key_filename, 'r') as f:
#             public_key = f.read()    
#     

