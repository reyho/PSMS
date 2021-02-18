'''
Uploader.py is responsible for the upload of the encrypted file.
'''
import os

class Uploader:

    def __init__(self, decrypted_response_request_url):
        self.__decrypted_HTTPS_response = decrypted_response_request_url["decrypted_response"]
        self.__request = decrypted_response_request_url["request"]
        self.__url = decrypted_response_request_url["url"]

    def upload_encrypted_file(self):
        if os.path.exists('user/encFile/file.enc'):
            with open('user/encFile/file.enc', 'rb') as f:
                payload = dict(value=self.__decrypted_HTTPS_response, mode='UPLOAD_FILE')
                files = {'upload_file': f}
                print('Starting upload ...')
                req = self.__request.post(self.__url, data=payload, files=files)
                print(req.text)
                del req
        else:
            print("There is no encrypted file to upload.")
            sys.exit(1) #If the encrypted file doesn't exists exit the program

    def upload_encrypted_key(self):
        if os.path.exists('user/symmKey/enc_aes_key.enc'):
            with open('user/symmKey/enc_aes_key.enc', 'rb') as f:
                payload = dict(value=self.__decrypted_HTTPS_response, mode='UPLOAD_KEY')
                files = {'upload_key': f}
                print('Starting upload ...')
                req = self.__request.post(self.__url, data=payload, files=files)
                print(req.text)
                del req
        else:
            print("There is no encrypted aes key to upload.")
            sys.exit(1) #If the encrypted aes key doesn't exists exit the program
