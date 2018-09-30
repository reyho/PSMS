from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import sys

class Cryptographer:

    def __init__(self, encrypted_file):
        self.__encrypted_file = encrypted_file

    def decrypt_file(self):
        Cryptographer.__load_priv_key(self)
        Cryptographer.__decrypt_file(self)
        return self.__decrypted_file

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

    def __decrypt_file(self):
        try:
            self.__decrypted_file = self.__private_key.decrypt(
                self.__encrypted_file,
                padding.PKCS1v15()
            )
        except Exception as e:
            print('Something went wrong with the decryption.')
            print(e)
            sys.exit(1)
