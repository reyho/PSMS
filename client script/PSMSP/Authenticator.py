from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import requests
import base64

class Authenicator:

    def __init__(self, url):
        self.url = url

    def download_file(self):
        s = requests.Session()
        response = s.get(self.url, stream=True)
        self.ciphertext = response.text
        self.ciphertext = base64.b64decode(self.ciphertext)
        del response
	
	def load_private_key(self):
		with open("private_key.pem", "rb") as key_file:

			private_key = serialization.load_pem_private_key(
				key_file.read(),
				password=None,
				backend=default_backend()
			)
