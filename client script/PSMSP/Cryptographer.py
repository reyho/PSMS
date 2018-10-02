from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import sys

class Cryptographer:

    def __init__(self):

        with open("user/symmKey/enc_aes_kljuc.enc", "rb") as symmKey_file:
            self.__encrypted_symmetric_key = symmKey_file.read()
        with open("user/encFile/kod.enc" ,"rb") as enc_file:
            self.__encrypted_file = enc_file.read()
        self.__salt = os.urandom(8)

    def decrypt_symmetric_key(self):
        Cryptographer.__load_priv_key(self)
        Cryptographer.__decrypt_symmetric_key(self)
        if os.path.exists('user/symmKey/aes_key.key'):
            with open("user/symmKey/aes_key.key", "wb") as decrypted_key:
                decrypted_key.write(self.__decrypted_symmetric_key)
        else:
            print('You have to download the key first!')
            sys.exit(1)

    def decrypt_file(self):
        Cryptographer.__decrypt_file(self)

    def __decrypt_file(self):
        Cryptographer.__get_and_remove_salt(self)
        Cryptographer.__get_key_and_iv(self, self.__salt)
        cipher = Cipher(algorithms.AES(self.__key), modes.CBC(self.__iv), backend=default_backend())
        decryptor = cipher.decryptor()
        with open("slika1.png", "wb") as dec_file:
            dec_file.write(decryptor.update(self.__encrypted_data) + decryptor.finalize())

    def encrypt_file(self):
        Cryptographer.__encrypt_file(self)

    def __get_and_remove_salt(self):
        with open("slika.enc", "rb") as enc_file:
            encrypted_file = enc_file.read()
        self.__salt = encrypted_file[:8]
        self.__encrypted_data = encrypted_file[8:]


    def __encrypt_file(self):
        Cryptographer.__get_key_and_iv(self, self.__salt)
        cipher = Cipher(algorithms.AES(self.__key), modes.CBC(self.__iv), backend=default_backend())
        encryptor = cipher.encryptor()
        with open("slika.enc", "wb") as enc_file:
            salt_and_padded_file = self.__salt + encryptor.update(Cryptographer.__padding_source(self)) + encryptor.finalize()
            enc_file.write(salt_and_padded_file)


    def __padding_source(self):
        padder = padding.PKCS7(128).padder()
        with open("slika.png", "rb") as source_file:
            return padder.update(source_file.read()) + padder.finalize()

    def __get_key_and_iv(self, salt):
        with open("aes.key", "rb") as key_file:
            aes_key = key_file.read()

        hashing = hashes.Hash(hashes.SHA512(), backend=default_backend())
        hashing.update(aes_key)
        hashing.update(salt)
        hashing_iv = hashing.copy()
        hashing_iv.update(hashing.finalize())
        hashing_key = hashing_iv.copy()
        hashed_iv = hashing_iv.finalize()
        hashing_key.update(salt)
        hashing_key.update(aes_key)
        hashing_key.update(hashed_iv)
        hashed_key = hashing_key.finalize()

        hashed_iv = bytes(hashed_iv)
        self.__iv = hashed_iv[:16]

        hashed_key = bytes(hashed_key)
        self.__key = hashed_key[:32]


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
