'''
The working python script
'''

#Importing the Authenticator and Downloader class
from PSMSP.Authenticator import Authenticator
from PSMSP.Downloader import Downloader
from PSMSP.Parser import Parser
from PSMSP.Cryptographer import Cryptographer

'''
parser = Parser()
command_line_args = parser.parse_command_line()
if command_line_args['mode'] == 'download':
    authenticator = Authenticator(command_line_args['url'])
    downloader = Downloader(authenticator.authenticate())
    downloader.download_encrypted_file()
'''
encrypted_file = open("enc_aes_kljuc.enc", "rb")
cryptographer = Cryptographer(encrypted_file.read())
decrypted_file = open("aes_key.key", "wb")
decrypted_file.write(cryptographer.decrypt_file())
