'''
Downloader.py is responsible for the download of the encrypted file
after the authentication process.
'''

from clint.textui import progress
import re

class Downloader:
    
    #Initialising the object with the decrypted response, request object, url, and error detection
    def __init__(self, decrypted_response_request_url_error):
        self.__decrypted_HTTP_response = decrypted_response_request_url_error["decrypted_response"]
        self.__request = decrypted_response_request_url_error["request"]
        self.__url = decrypted_response_request_url_error["url"]
    
    #Sending the decrypted response to the server and downloading the encrypted file    
    def download_encrypted_file(self): 
        try:
            HTTP_response = self.__request.get(self.__url, params={'value': self.__decrypted_HTTP_response, 'mode': 'DOWNLOAD'}, stream=True)
        except Exception as e:
            print('HTTP request error in Downloader.')
            print(e)
            sys.exit(1)
        file_name = Downloader.__get_filename_from_cd(self, HTTP_response.headers.get('content-disposition'))
        #Download with progress bar
        with open(file_name, 'wb') as f:
            total_length = int(HTTP_response.headers.get('content-length'))
            for chunk in progress.bar(HTTP_response.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()
        del HTTP_response        
            
    #Getting the file name of the downloading file from header "content-disposition".
    def __get_filename_from_cd(self, cd):
        file_name = re.findall('filename="(.+)"', cd)
        if len(file_name) == 0:
            return 'Untitled.enc'
        return file_name[0]