from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import requests
import base64

class Authenicated_download:

    def __init__(self, url):
        self.url = url

    def download_file(self):
        s = requests.Session()
        response = s.get(url, stream=True)
        ciphertext = response.text
        ciphertext = base64.b64decode(ciphertext)
        del response
