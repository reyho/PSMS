'''
Downloader.py is responsible for the download of the encrypted file
after the authentication process.
'''

from clint.textui import progress
import os
import re

class Downloader:

    #Initialising the object with the decrypted response, request object and url
    def __init__(self, decrypted_response_request_url):
        self.__decrypted_HTTPS_response = decrypted_response_request_url["decrypted_response"]
        self.__request = decrypted_response_request_url["request"]
        self.__url = decrypted_response_request_url["url"]

    #Sending the decrypted response to the server and downloading the encrypted file
    def download_encrypted_file(self):
        try:
            HTTPS_response = self.__request.get(self.__url, params={'value': self.__decrypted_HTTPS_response, 'mode': 'DOWNLOAD_FILE'}, stream=True)
        except Exception as e:
            print('HTTPS request error in Downloader.')
            print(e)
            sys.exit(1)
        if not os.path.exists('user/encFile'):
            os.mkdir('user/encFile')
        file_name = 'user/encFile/' +  Downloader.__get_filename_from_cd(self, HTTPS_response.headers.get('content-disposition'))        
        #Download with progress bar
        with open(file_name, 'wb') as f:
            total_length = int(HTTPS_response.headers.get('content-length'))
            for chunk in progress.bar(HTTPS_response.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()
        del HTTPS_response
        
    def download_encrypted_key(self):
        try:
            HTTPS_response = self.__request.get(self.__url, params={'value': self.__decrypted_HTTPS_response, 'mode': 'DOWNLOAD_KEY'}, stream=True)
        except Exception as e:
            print('HTTPS request error in Downloader.')
            print(e)
            sys.exit(1)
        if not os.path.exists('user/symmKey'):
            os.mkdir('user/symmKey')
        file_name = 'user/symmKey/' +  Downloader.__get_filename_from_cd(self, HTTPS_response.headers.get('content-disposition'))
        #Download with progress bar
        with open(file_name, 'wb') as f:
            total_length = int(HTTPS_response.headers.get('content-length'))
            for chunk in progress.bar(HTTPS_response.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()
        del HTTPS_response

    #Getting the file name of the downloading file from header "content-disposition".
    def __get_filename_from_cd(self, cd):
        file_name = re.findall('filename="(.+)"', cd)
        if len(file_name) == 0:
            return 'Untitled.enc'
        return file_name[0]
