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

    def decrypt_symmetric_key(self, path, materialize=False):
        #Decrypting the symmetric key with a RSA private key
        self.__materialize = materialize #The boolean that controls if the symmetric key will be written to a file or used only in a variable for cryptograhy
        Cryptographer.__load_priv_key(self, path)
        Cryptographer.__decrypt_symmetric_key(self) #Calling the function that actually decrypts the symmetric key
        if materialize:
            with open("user/symmKey/aes_key.key", "wb") as decrypted_key:
                decrypted_key.write(self.__decrypted_symmetric_key) #Writing the symetric key to a file.

    def encrypt_symmetric_key(self, path):
        #Encrypting the symmetric key with a RSA public key
        Cryptographer.__load_priv_key(self, path)
        Cryptographer.__encrypt_symmetric_key(self) #Calling the function that actually encrypts the symmetric key
        with open("user/symmKey/enc_aes_key.enc", "wb") as encrypted_key:
            encrypted_key.write(self.__encrypted_symmetric_key) #Writing the encrypted symetric key to a file.
        os.remove("user/symmKey/aes_key.key") #Deleting the symmetric key after encryption

    def decrypt_file(self):
        Cryptographer.__get_and_remove_salt(self) #Extracting the salt from the final encrypted file and removing it so it can be decrypted
        Cryptographer.__get_key_and_iv(self, self.__salt) #Calculating the key and iv from the result of hashing the salt value and symmetric key
        cipher = Cipher(algorithms.AES(self.__key), modes.CBC(self.__iv), backend=default_backend())
        decryptor = cipher.decryptor()
        with open("ziped.zip", "wb") as dec_file:
            dec_file.write(decryptor.update(self.__encrypted_data) + decryptor.finalize()) #Writing the decrypted data temporaly to a file as .zip
        os.remove("user/encFile/file.enc") #Removing the encrypted file

    def __get_and_remove_salt(self):
        if os.path.exists('user/encFile/file.enc'):
            with open("user/encFile/file.enc", "rb") as enc_file:
                encrypted_file = enc_file.read()
            self.__salt = encrypted_file[:8] #First 8 bytes are the salt which are extracted from the file
            self.__encrypted_data = encrypted_file[8:] #The file for decryption excludes the first 8 bytes
        else:
            print("There is no encrypted file to decrypt.")
            sys.exit(1) #If the encrypted file doesn't exists exit the program

    def encrypt_file(self):
        Cryptographer.__get_key_and_iv(self, self.__salt) #For encryption I use a newly random value salt for key and iv generation
        cipher = Cipher(algorithms.AES(self.__key), modes.CBC(self.__iv), backend=default_backend())
        encryptor = cipher.encryptor()
        with open("user/encFile/file.enc", "wb") as enc_file:
            #Writing the salt + encrypted .zip file to a .enc file
            salt_and_padded_file = self.__salt + encryptor.update(Cryptographer.__padding_source(self)) + encryptor.finalize()
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

    def __get_key_and_iv(self, salt):
        #With this function i decide if I pass the symm key read from a file or from a variable to the __hash_away function
        if self.__materialize:
            with open("user/symmKey/aes_key.key", "rb") as key_file:
                aes_key = key_file.read()
        else:
            aes_key = self.__decrypted_symmetric_key

        Cryptographer.__hash_away(self, aes_key, self.__salt)


    def __load_priv_key(self, path):
        #Loading the RSA private key
        try:
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
            print("There is no symmetric key for encryption.")
            sys.exit(1)
