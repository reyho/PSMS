'''
Cryptographer.py takes care of the encryption/decryption of the symmetric key and
the files that store your security information.
'''

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
        #Initialising the salt value with random 8 bytes
        self.__salt = os.urandom(8)

    def decrypt_symmetric_key(self, path, target, materialize=False):
        #Decrypting the symmetric key with a RSA private key
        self.__load_priv_key(path)
        self.__rsa_decryption(target) #Calling the function that actually decrypts the symmetric key
        if materialize: #The boolean that controls if the symmetric key will be written to a file or used only in a variable for cryptograhy
            with open("user/symmKey/aes_key.key", "wb") as decrypted_key:
                decrypted_key.write(self.__decrypted_message) #Writing the symetric key to a file.
            os.remove("user/symmKey/enc_aes_key.enc")

    def decrypt_passwords(self, path, target):
        # decrypting the passwords
        self.__load_priv_key(path)
        self.__rsa_decryption(target)
        return self.__decrypted_message


    def encrypt_symmetric_key(self, path, target):
        #Encrypting the symmetric key with a RSA public key
        self.__load_priv_key(path)
        self.__rsa_encryption(target) #Calling the function that actually encrypts the symmetric key
        with open("user/symmKey/enc_aes_key.enc", "wb") as encrypted_key:
            encrypted_key.write(self.__encrypted_symmetric_key) #Writing the encrypted symetric key to a file.
        os.remove("user/symmKey/aes_key.key") #Deleting the symmetric key after encryption

    def encrypt_passwords(self, path, target):
        # encrypting the passwords
        self.__load_priv_key(path)
        self.__rsa_encryption(target)


    def decrypt_file(self,path):
        self.decrypt_symmetric_key(path, 'user/symmKey/enc_aes_key.enc') # Decrypting the symmetric key
        self.__get_and_remove_salt() #Extracting the salt from the final encrypted file and removing it so it can be decrypted
        self.__hash_away(self.__decrypted_message, self.__salt) #Calculating the key and iv from the result of hashing the salt value and symmetric key
        cipher = Cipher(algorithms.AES(self.__key), modes.CBC(self.__iv), backend=default_backend())
        decryptor = cipher.decryptor()
        with open("ziped.zip", "wb") as dec_file:
            dec_file.write(decryptor.update(self.__encrypted_data) + decryptor.finalize()) #Writing the decrypted data temporaly to a file as .zip

    def __get_and_remove_salt(self):
        if os.path.exists('user/encFile/file.enc'):
            with open("user/encFile/file.enc", "rb") as enc_file:
                encrypted_file = enc_file.read()
            self.__salt = encrypted_file[:8] #First 8 bytes are the salt which are extracted from the file
            self.__encrypted_data = encrypted_file[8:] #The file for decryption excludes the first 8 bytes
        else:
            print("There is no encrypted file to decrypt.")
            sys.exit(1) #If the encrypted file doesn't exists exit the program

    def encrypt_file(self,path):
        self.decrypt_symmetric_key(path, 'user/symmKey/enc_aes_key.enc') # Decrypting the symmetric key
        self.__hash_away(self.__decrypted_message, self.__salt) #For encryption I use a newly random value salt for key and iv generation
        cipher = Cipher(algorithms.AES(self.__key), modes.CBC(self.__iv), backend=default_backend())
        encryptor = cipher.encryptor()
        with open("user/encFile/file.enc", "wb") as enc_file:
            #Writing the salt + encrypted .zip file to a .enc file
            salt_and_padded_file = self.__salt + encryptor.update(self.__padding_source()) + encryptor.finalize()
            enc_file.write(salt_and_padded_file)
        os.remove("ziped.zip")
        for root, dirs, files in os.walk('user/secFiles'):
            #Deleting all files and subfolders of secFiles/ without deleting secFiles/
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))


    def __padding_source(self):
        #Adding a symmetric padding to the .zip file so it can be encrypted
        padder = padding.PKCS7(128).padder()
        with open("ziped.zip", "rb") as source_file:
            return padder.update(source_file.read()) + padder.finalize()

    def __hash_away(self, aes_key, salt):
        #This is the algorithm with whom I generate the 256 bit key and iv for symmetric cryptography
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

        self.__iv = hashed_iv[:16]
        self.__key = hashed_key[:32]

    def __load_priv_key(self, path):
        #Loading the RSA private key
        if os.path.exists(path):
            try:
                with open(path, "rb") as key_file:
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

    def __rsa_decryption(self, target):
        if os.path.exists(target):
            with open(target, 'rb') as enc_key:
                try:
                    self.__decrypted_message = self.__private_key.decrypt(
                        enc_key.read(),
                        apadding.OAEP(
                                mgf=apadding.MGF1(algorithm=hashes.SHA512()),
                                algorithm=hashes.SHA512(),
                                label=None
                            )
                    )
                except Exception as e:
                    print('Something went wrong with the RSA decryption')
                    print(e)
                    sys.exit(1)
        else:
            print("There is no target for the RSA decryption.")
            sys.exit(1)


    def __rsa_encryption(self, target):
        public_key = self.__private_key.public_key()
        if os.path.exists(target):
            with open(target, 'rb') as dec_key:
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
                    print('Something went wrong with the RSA encryption.')
                    print(e)
                    sys.exit(1)
        else:
            print("There is no target for the RSA encryption.")
            sys.exit(1)
