'''
Generator.py generates a RSA public key pair.
'''

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

class Generator:

    def generate_key_pair(self, path):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )

        public_key = private_key.public_key()

        pem_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        pem_public = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open(path + "private_key.pem", "wb") as privateKey:
            privateKey.write(pem_private)

        with open(path + "public_key.pem", "wb") as publicKey:
            publicKey.write(pem_public)

    def generate_aes_key(self,path):

        key = os.urandom(256)
        with open(path + "aes_key.key", "wb") as aesKey:
            aesKey.write(key)
