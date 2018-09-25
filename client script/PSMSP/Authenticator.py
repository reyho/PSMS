from os import path
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import requests
import base64

class Authenticator:

    s = requests.Session()

    def __init__(self, url):
        self.url = url

    def load_priv_key(self):
        with open("C:\git\PSMS\keys\private_key.pem", "rb") as key_file:
            self.private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())

    def get_ciphertext(self):
        response = Authenticator.s.get(self.url, stream=True)
        self.ciphertext = response.text
        self.ciphertext = base64.b64decode(self.ciphertext)
        del response

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

    def validate_message(self, url, decrypted_message):
        response = Authenticator.s.get(url, params={'value': decrypted_message}, stream=True)
        print(response.text)
        del response
