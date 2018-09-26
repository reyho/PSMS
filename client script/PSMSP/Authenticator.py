'''
This is the module who is responsible for the authentication to the server 
and fetching the encrypted files from the server afterwards.
'''

from os import path
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import requests
import base64

class Authenticator:
	
	#Declaration of the HTTP request with session enabled
    s = requests.Session()
	
	#Initialising the object with the url of the php script 
	#whitch will authenticate you with an RSA key pair
    def __init__(self, url):
        self.url = url
	
	#Loading the private key which we will use to decrypt the response of
	#the server in order to authenticate us
    def load_priv_key(self):
		#I have to find a better way to pass the path of the private key
        with open("C:\git\PSMS\keys\private_key.pem", "rb") as key_file:
            self.private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())
	
	#Getting and storing the encrypted response used for authentication
    def get_ciphertext(self):
        response = Authenticator.s.get(self.url, stream=True)
        self.ciphertext = response.text
        self.ciphertext = base64.b64decode(self.ciphertext)
        del response
		
	#Decrypting the response of the server with the private key
	#and returning the decrypted response
    def decrypt_message(self):
        decrypted_response = self.private_key.decrypt(
    		self.ciphertext,
    		padding.OAEP(
    			mgf=padding.MGF1(algorithm=hashes.SHA1()),
    			algorithm=hashes.SHA1(),
    			label=None
    		)
    	)
        return decrypted_response
	
	#Sending the decrypted response back to the server in order to
	#autenticate ourselfs and download the encrypted files.
	'''
	I have to find a better way to pass the path of the php script
	which will take the decrypted response and allow me to download
	the encrypted files. Maybe I should do this with one php script
	to which i will pass an argument who lets the php script know
	what I want to do with the script.
	'''
    def validate_message(self, url, decrypted_message):
        response = Authenticator.s.get(url, params={'value': decrypted_message}, stream=True)
        print(response.text)
        del response
