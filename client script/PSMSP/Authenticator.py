'''
This is the module who is responsible for the authentication to the server 
and fetching the encrypted files from the server afterwards.
'''

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import sys
import requests
import base64

class Authenticator:
    #Declaration of the HTTP request with session enabled
    __HTTP_request = requests.Session()
	
    #Initialising the object with the url of the php script whitch will authenticate me
    def __init__(self, url):
        self.__url = url
    
    def authenticate(self):
        #Loading the private key which I will use to decrypt the response of the server in order to authenticate me.
        Authenticator.__load_priv_key(self)
        
        #Getting and storing the encrypted random number used for authentication 
        Authenticator.__get_encrypted_message(self)
        
        #Decrypting the random number with the private key 
        Authenticator.__decrypt_message(self)
        
        #Returning the decrypted response, request object and url so that the session is maintained                
        return dict(
            decrypted_response=self.__decrypted_HTTP_response, 
            request=Authenticator.__HTTP_request, 
            url=self.__url
        )
    
    def __load_priv_key(self):
        try:
            #Maybe I should make a config file to host the relevant data like paths and such.
            with open("../keys/private_key.pem", "rb") as key_file:
                self.__private_key = serialization.load_pem_private_key(
                    key_file.read(), 
                    password=None, 
                    backend=default_backend()
                )
        except Exception as e:            
            print('Private key could not be found.')
            print(e)
            sys.exit(1)
    
    def __get_encrypted_message(self):
        try:
            HTTP_response = Authenticator.__HTTP_request.get(
                self.__url, 
                params={'mode': 'AUTHENTICATION'}, 
                stream=True
            )
        except requests.exceptions.RequestException as e:
            print('HTTP request error in Authenticator.')
            print(e)
            sys.exit(1)        
        self.__ciphertext = HTTP_response.text
        self.__ciphertext = base64.b64decode(self.__ciphertext)
        del HTTP_response
            
    def __decrypt_message(self):
        try:
            self.__decrypted_HTTP_response = self.__private_key.decrypt(
                self.__ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA1()),
                    algorithm=hashes.SHA1(),
                    label=None
                )
            )
        except Exception as e:
            print('Something went wrong with the decryption.')
            print(e)
            sys.exit(1)