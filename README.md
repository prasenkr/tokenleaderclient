# tokenleader-client

thoughts about  functionallities
tokenleader-client
-----------------
reads credentials from  /etc/tokenleader.yml  , also have auth_url = token_leader_url 
sends these credential to token leader to get token
use session ?

accepts token as  python parameter and also from cli and sends it to tokenleader for verifiaction
if expired token , should read the users credentials from file and get a fresh token
returns verification result 

token admin operation for user and role registration , org, dept and other db opertaions

should support https and certificates
python-pkg with cli facility for getting token
it should be a dependency  pkg to other microservices
other microsrrvies should be able to import and use it 

