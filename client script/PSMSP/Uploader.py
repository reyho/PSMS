'''
Uploader.py is responsible for the upload of the encrypted file.
'''

class Uploader:

    def __init__(self, decrypted_response_request_url):
        self.__decrypted_HTTPS_response = decrypted_response_request_url["decrypted_response"]
        self.__request = decrypted_response_request_url["request"]
        self.__url = decrypted_response_request_url["url"]

    def upload_encrypted_file(self):
        with open('user/encFile/file.enc', 'rb') as f:
            payload = dict(value=self.__decrypted_HTTPS_response, mode='UPLOAD_FILE')
            files = {'upload_file': f}
            req = self.__request.post(self.__url, data=payload, files=files)
            print(req.text)
            del req
