# tokenleader-client

an installable client which reads user's credential from a text file  or from users   
os environment ( not yet implemented) and initialize a client. 

The configuration file is divided into two files . 
config/general_config.yml which holds the non secret configs  about the client and looks as

		user_auth_info_from: file # OSENV or file  
		user_auth_info_file_location: tests/testdata/test_settings.ini ===> users auth information  
		fernet_key_file: tests/testdata/farnetkey ====> keep this in a different location than the  ini file  
		tl_public_key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCYV9y94je6Z9N0iarh0xNrE3IFGrdktV2TLfI5h60hfd9yO7L9BZtd94/r2L6VGFSwT/dhBR//CwkIuue3RW23nbm2OIYsmsijBSHtm1/2tw/0g0UbbneM9vFt9ciCjdq3W4VY8I6iQ7s7v98qrtRxhqLc/rH2MmfERhQaMQPaSnMaB59R46xCtCnsJ+OoZs5XhGOJXJz8YKuCw4gUs4soRMb7+k7F4wADseoYuwtVLoEmSC+ikbmPZNWOY18HxNrSVJOvMH2sCoewY6/GgS/5s1zlWBwV/F0UvmKoCTf0KcNHcdzXbeDU9/PkGU/uItRYVfXIWYJVQZBveu7BYJDR bhujay@DESKTOP-DTA1VEB

the other file , which is user_auth_info_file_location: tests/testdata/test_settings.ini   holds the   
users authentiaction information . The file is generated using  an cli   

./userconfig.sh  -u user1 -p user1 --url http://localhost:5001    

the file  look like this :    

		[DEFAULT]  
		tl_user = user1  
		tl_url = http://localhost:5001  
		tl_password = gAAAAABcYnpRqet_VEucowJrE0lM1RQh2j5E-_Al4j8hm8vJaMvfj2nk7yb3zQo95lBFDoDR_CeoHVRY3QBFFG-p9Ga4bkJKBw==

note that the  original password has been encrypted before  saving in the file. if the keyfile is lost or the 
password is forgotten   the  file has to be deleted and recreated. Accordingly the users password in the 
tokenleader server also to be changed.

after downloading the client from  https://github.com/microservice-tsp-billing/tokenleader-client  
create a venv :   tokenleader-client$ virtualenv -p python3 venv   
pip install -r requirement.txt 

then from python shell it works as follows  

		>>> from  client.client import Client  
		>>> c = Client()
		>>> c.get_token()
		{'message': 'success', 'status': 'success', 'auth_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJpYXQiOjE1NDk5NjcxODAsImV4cCI6MTU0OTk3MDc4MCwic3ViIjp7IndmYyI6eyJvcmd1bml0Ijoib3UxIiwibmFtZSI6IndmYzEiLCJkZXBhcnRtZW50IjoiZGVwdDEiLCJpZCI6MSwib3JnIjoib3JnMSJ9LCJlbWFpbCI6InVzZXIxIiwiaWQiOjEsInVzZXJuYW1lIjoidXNlcjEiLCJyb2xlcyI6WyJyb2xlMSJdfX0.gzW0GlgR9qiNLZbR-upuzgHMw5rOm2luV-EnHZwlOSJ-0kJnHsiiT5Wk-HZaqMGZd0YJxA1e9GMroHixtj7WJsbLLjhgqQ5H1ZprCkA9um6-vdkwAFVduWIqIN7S6LbsE036bN7y4cdgVhuJAKoiV1KyxOU1-Hxid5l3inL0Hx2aDUrZ3InzFKBw7Mll86xWdfkpHSdyVjVuayKQMvH2IdT3N15k4O2tSwV3t6UhG6MO0ngHFt3LFR471QWGzJ8UyRzqyqbheuk5vwPk684MfRclCtKx33LWAMf-HXQgVA2py_NzmEiY1ROsKmZqpbIO9YKIO_aFCmzB7DQSI8dcYg', 'service_catalog': {'tokenleader': {'endpoint_url_external': 'localhost:5001', 'endpoint_url_admin': None, 'id': 2, 'endpoint_url_internal': None, 'name': 'tokenleader'}, 'micros1': {'endpoint_url_external': 'localhost:5002', 'endpoint_url_admin': None, 'id': 1, 'endpoint_url_internal': None, 'name': 'micros1'}}}
		>>> c.verify_token('eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJpYXQiOjE1NDk5NjcxODAsImV4cCI6MTU0OTk3MDc4MCwic3ViIjp7IndmYyI6eyJvcmd1bml0Ijoib3UxIiwibmFtZSI6IndmYzEiLCJkZXBhcnRtZW50IjoiZGVwdDEiLCJpZCI6MSwib3JnIjoib3JnMSJ9LCJlbWFpbCI6InVzZXIxIiwiaWQiOjEsInVzZXJuYW1lIjoidXNlcjEiLCJyb2xlcyI6WyJyb2xlMSJdfX0.gzW0GlgR9qiNLZbR-upuzgHMw5rOm2luV-EnHZwlOSJ-0kJnHsiiT5Wk-HZaqMGZd0YJxA1e9GMroHixtj7WJsbLLjhgqQ5H1ZprCkA9um6-vdkwAFVduWIqIN7S6LbsE036bN7y4cdgVhuJAKoiV1KyxOU1-Hxid5l3inL0Hx2aDUrZ3InzFKBw7Mll86xWdfkpHSdyVjVuayKQMvH2IdT3N15k4O2tSwV3t6UhG6MO0ngHFt3LFR471QWGzJ8UyRzqyqbheuk5vwPk684MfRclCtKx33LWAMf-HXQgVA2py_NzmEiY1ROsKmZqpbIO9YKIO_aFCmzB7DQSI8dcYg')
		{'payload': {'iat': 1549967180, 'exp': 1549970780, 'sub': {'username': 'user1', 'roles': ['role1'], 'id': 1, 'email': 'user1', 'wfc': {'orgunit': 'ou1', 'id': 1, 'org': 'org1', 'department': 'dept1', 'name': 'wfc1'}}}, 'message': 'Token has been successfully decrypted', 'status': 'Verification Successful'}
		>>>







thoughts about  functionallities
tokenleader-client
-----------------

1) integrate rbac inside the client
2) make the client an installable pkg 
3) extend user creation/ catalog creation  etc. as part of the client  
4) develop client for micros1  - which will make it easier to understand how  other microservice  should be developed keeping token leader in mind.  Target one week.


if expired token , should read the users credentials from file and get a fresh token
returns verification result 

token admin operation for user and role registration , org, dept and other db opertaions

should support https and certificates
python-pkg with cli facility for getting token
it should be a dependency  pkg to other microservices
other microsrrvies should be able to import and use it 

