from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import sys

class Cryptographer:

    def __init__(self):
        '''with open("user/symmKey/enc_aes_kljuc.enc", "rb") as symmKey_file:
            self.__encrypted_symmetric_key = symmKey_file.read()
        with open("user/encFile/kod.enc" ,"rb") as enc_file:
            self.__encrypted_file = enc_file.read()'''
        self.__salt = os.urandom(8)

    def decrypt_symmetric_key(self):
        Cryptographer.__load_priv_key(self)
        Cryptographer.__decrypt_symmetric_key(self)
        with open("user/symmKey/aes_key.key", "wb") as decrypted_key:
            decrypted_key.write(self.__decrypted_symmetric_key)

    #def decrypt_file(self):


    #def __decrypt_file(self):
    
    def encrypt_file(self):
        Cryptographer.__encrypt_file(self)
    
    def __encrypt_file(self):
        Cryptographer.__get_key_and_iv(self)
        cipher = Cipher(algorithms.AES(self.__key), modes.CBC(self.__iv), backend=default_backend())
        encryptor = cipher.encryptor()
        with open("slika.png", "rb") as source_file:
            with open("slika.enc", "wb") as enc_file:
                enc_file.write(encryptor.update(source_file.read()) + encryptor.finalize())
        
    
    def __get_key_and_iv(self):
        with open("aes.key", "rb") as key_file:
            aes_key = key_file.read()
            
        hashing = hashes.Hash(hashes.SHA512(), backend=default_backend())
        hashing.update(aes_key)
        hashing.update(self.__salt)
        hashing_iv = hashing.copy()
        hashing_iv.update(hashing.finalize())
        hashing_key = hashing_iv.copy()
        hashed_iv = hashing_iv.finalize()
        hashing_key.update(self.__salt)
        hashing_key.update(aes_key)
        hashing_key.update(hashed_iv)
        hashed_key = hashing_key.finalize()
        
        hashed_iv = bytes(hashed_iv)
        x = 0
        self.__iv = b''
        while x < 16:
            self.__iv += hashed_iv[x].to_bytes(1, byteorder='big')
            x += 1
            
        hashed_key = bytes(hashed_key)
        x = 0
        self.__key = b''
        while x < 32:
            self.__key += hashed_key[x].to_bytes(1, byteorder='big')
            x += 1


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

    def __decrypt_symmetric_key(self):
        try:
            self.__decrypted_symmetric_key = self.__private_key.decrypt(
                self.__encrypted_symmetric_key,
                padding.PKCS1v15()
            )
        except Exception as e:
            print('Something went wrong with the decryption.')
            print(e)
            sys.exit(1)
