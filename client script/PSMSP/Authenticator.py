'''
This is the module who is responsible for the authentication to the server 
and fetching the encrypted files from the server afterwards.
'''

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import requests
import base64

'''
I have to implement some error handling in case the authentication
fails or something went wrong with the server.
'''

class Authenticator:
    #Declaration of the HTTP request with session enabled
    request = requests.Session()
	
    #Initialising the object with the url of the php script
    #whitch will authenticate you with an RSA key pair
    def __init__(self, url):
        self.url = url        
    
    def authenticate(self):
        #Loading the private key which we will use to decrypt the response of
        #the server in order to authenticate us.
        #I have to find a better way to pass the path of the private key.
        with open("C:\git\PSMS\keys\private_key.pem", "rb") as key_file:
            self.private_key = serialization.load_pem_private_key(
                key_file.read(), 
                password=None, 
                backend=default_backend())
        
        #Getting and storing the encrypted response used for authentication        
        response = Authenticator.request.get(self.url, params={'mode': 'AUTHENTICATION'}, stream=True)
        self.ciphertext = response.text
        self.ciphertext = base64.b64decode(self.ciphertext)
        del response
        
        #Decrypting the response of the server with the private key
        #and returning the decrypted response and the request object
        #so that the session works
        decrypted_response = self.private_key.decrypt(
    		self.ciphertext,
    		padding.OAEP(
    			mgf=padding.MGF1(algorithm=hashes.SHA1()),
    			algorithm=hashes.SHA1(),
    			label=None
    		)
    	)
        return dict(deced_resp=decrypted_response, req=Authenticator.request, url=self.url)
