from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as apadding
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import sys
import shutil

class Cryptographer:

    def __init__(self):
        self.__salt = os.urandom(8)

    def decrypt_symmetric_key(self, path):
        Cryptographer.__load_priv_key(self, path)
        Cryptographer.__decrypt_symmetric_key(self)
        with open("user/symmKey/aes_key.key", "wb") as decrypted_key:
            decrypted_key.write(self.__decrypted_symmetric_key)
        
    def encrypt_symmetric_key(self, path):
        Cryptographer.__load_priv_key(self, path)
        Cryptographer.__encrypt_symmetric_key(self)
        with open("user/symmKey/enc_aes_key.enc", "wb") as encrypted_key:
            encrypted_key.write(self.__encrypted_symmetric_key)
        os.remove("user/symmKey/aes_key.key")

    def decrypt_file(self):
        Cryptographer.__get_and_remove_salt(self)
        Cryptographer.__get_key_and_iv(self, self.__salt)
        cipher = Cipher(algorithms.AES(self.__key), modes.CBC(self.__iv), backend=default_backend())
        decryptor = cipher.decryptor()
        with open("ziped.zip", "wb") as dec_file:
            dec_file.write(decryptor.update(self.__encrypted_data) + decryptor.finalize())
        os.remove("user/symmKey/aes_key.key")
        os.remove("user/encFile/file.enc")
            
    def __get_and_remove_salt(self):
        if os.path.exists('user/encFile/file.enc'):
            with open("user/encFile/file.enc", "rb") as enc_file:
                encrypted_file = enc_file.read()
            self.__salt = encrypted_file[:8]
            self.__encrypted_data = encrypted_file[8:]
        else:
            print("There is no encrypted file to decrypt.")
            sys.exit(1)

    def encrypt_file(self):
        Cryptographer.__get_key_and_iv(self, self.__salt)
        cipher = Cipher(algorithms.AES(self.__key), modes.CBC(self.__iv), backend=default_backend())
        encryptor = cipher.encryptor()
        if not os.path.exists('user/encFile'):
            os.mkdir('user/encFile/')
        with open("user/encFile/file.enc", "wb") as enc_file:
            salt_and_padded_file = self.__salt + encryptor.update(Cryptographer.__padding_source(self)) + encryptor.finalize()
            enc_file.write(salt_and_padded_file)
        os.remove("user/symmKey/aes_key.key")
        os.remove("ziped.zip")
        shutil.rmtree("user/secFiles")


    def __padding_source(self):
        padder = padding.PKCS7(128).padder()
        with open("ziped.zip", "rb") as source_file:
            return padder.update(source_file.read()) + padder.finalize()

    def __get_key_and_iv(self, salt):
        with open("user/symmKey/aes_key.key", "rb") as key_file:
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


    def __load_priv_key(self, path):
        try:
            #Maybe I should make a config file to host the relevant data like paths and such.
            with open(path, "rb") as key_file:
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
        if os.path.exists('user/symmKey/enc_aes_key.enc'):
            with open('user/symmKey/enc_aes_key.enc', 'rb') as enc_key:
                try:
                    self.__decrypted_symmetric_key = self.__private_key.decrypt(
                        enc_key.read(),
                        apadding.OAEP(
                                mgf=apadding.MGF1(algorithm=hashes.SHA512()),
                                algorithm=hashes.SHA512(),
                                label=None
                            )
                    )
                except Exception as e:
                    print('Something went wrong with the decryption of the symmetric key.')
                    print(e)
                    sys.exit(1)
        else:
            print("There is no symmetric key for decryption.")
            sys.exit(1)
        
        
    def __encrypt_symmetric_key(self):
        public_key = self.__private_key.public_key()
        if os.path.exists('user/symmKey/aes_key.key'):
            with open('user/symmKey/aes_key.key', 'rb') as dec_key:
                try:
                    self.__encrypted_symmetric_key = public_key.encrypt(
                        dec_key.read(),
                        apadding.OAEP(
                            mgf=apadding.MGF1(algorithm=hashes.SHA512()),
                            algorithm=hashes.SHA512(),
                            label=None
                        )
                    )
                except Exception as e:
                    print('Something went wrong with the encryption of the symmetric key.')
                    print(e)
                    sys.exit(1)
        else:
            print("There is no symmetric key for decryption.")
            sys.exit(1)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
