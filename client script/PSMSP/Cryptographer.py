from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import sys

class Cryptographer:

    def __init__(self, encrypted_key):
        self.__encrypted_key = encrypted_key

    def decrypt_key(self):
        Cryptographer.__load_priv_key(self)
        Cryptographer.__decrypt_key(self)
        return self.__decrypted_file
        
    def decrypt_file(self):
        
    
    def __decrypt_file(self):
        
    
    def __load_priv_key(self):
        try:
            #Maybe I should make a config file to host the relevant data like paths and such.
            with open("F:/privateKey.pem", "rb") as key_file:
                self.__private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )
        except Exception as e:
            print('Private key could not be found.')
            print(e)
            sys.exit(1)

    def __decrypt_key(self):
        try:
            self.__decrypted_key = self.__private_key.decrypt(
                self.__encrypted_key,
                padding.PKCS1v15()
            )
        except Exception as e:
            print('Something went wrong with the decryption.')
            print(e)
            sys.exit(1)
