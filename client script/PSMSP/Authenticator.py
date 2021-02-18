'''
This is the module who is responsible for the authentication to the server
and fetching the encrypted files from the server afterwards.
'''

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import os
import sys
import requests #By default, SSL verification is enabled.
import base64

class Authenticator:
    #Declaration of the HTTP request with session enabled
    __HTTPS_request = requests.Session()

    #Initialising the object with the url of the php script whitch will authenticate me and the path to the private key
    def __init__(self, url, path):
        self.__url = url
        self.__path = path

    def authenticate(self):
        #Loading the private key which I will use to decrypt the response of the server in order to authenticate me.
        self.__load_priv_key()

        #Getting and storing the encrypted random number used for authentication
        self.__get_encrypted_message()

        #Decrypting the random number with the private key
        self.__decrypt_message()

        #Returning the decrypted response, request object and url so that the session is maintained
        return dict(
            decrypted_response=self.__decrypted_HTTPS_response,
            request=self.__HTTPS_request,
            url=self.__url
        )

    def __load_priv_key(self):
        if os.path.exists(self.__path):
            try:
                with open(self.__path, "rb") as key_file:
                    self.__private_key = serialization.load_pem_private_key(
                        key_file.read(),
                        password=None,
                        backend=default_backend()
                    )
            except Exception as e:
                print('Something went wrong with the loading of the private key.')
                print(e)
                sys.exit(1)
        else:
            print("There is no Private key to be loaded.")
            sys.exit(1)

    def __get_encrypted_message(self):
        try:
            HTTPS_response = self.__HTTPS_request.get(
                self.__url,
                params={'mode': 'AUTHENTICATION'},
                stream=True
            )
        except requests.exceptions.RequestException as e:
            print('HTTP request error in Authenticator.')
            print(e)
            sys.exit(1)
        self.__ciphertext = HTTPS_response.text
        self.__ciphertext = base64.b64decode(self.__ciphertext)
        del HTTPS_response

    def __decrypt_message(self):
        try:
            self.__decrypted_HTTPS_response = self.__private_key.decrypt(
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
