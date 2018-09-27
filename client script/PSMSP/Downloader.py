'''
Downloader.py is responsible for the download of the encrypted file
after the authentication process.
'''

import re

class Downloader:
        
    '''
    I have to find a better way to pass the path of the php script
    which will take the decrypted response and allow me to download
    the encrypted files. Maybe I should do this with one php script
    to which i will pass an argument who lets the php script know
    what I want to do with the script.
    '''	
    
    #Initialising the object with the decrypted response
    #and the request object.
    def __init__(self, deced_resp_req):
        self.decrypted_response = deced_resp_req["deced_resp"]
        self.request = deced_resp_req["req"]
        self.url = deced_resp_req["url"]
    
    #Sending the decrypted response to the server
    #and downloading the encrypted file
    
    def download_encrypted_file(self):
        response = self.request.get(self.url, params={'value': self.decrypted_response, 'mode': 'DOWNLOAD'}, stream=True)
        file_name = Downloader.get_filename_from_cd(response.headers.get('content-disposition'))
        open(file_name, 'wb').write(response.content)
        del response
    
    #Getting the file name of the downloading file from
    #the header "content-disposition".
    def get_filename_from_cd(cd):
        file_name = re.findall('filename="(.+)"', cd)
        if len(file_name) == 0:
            return None
        return file_name[0]