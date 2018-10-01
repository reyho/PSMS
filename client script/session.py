'''
The working python script
'''

#Importing the Authenticator and Downloader class
from PSMSP.Authenticator import Authenticator
from PSMSP.Downloader import Downloader
from PSMSP.Parser import Parser
from PSMSP.Cryptographer import Cryptographer


parser = Parser()
command_line_args = parser.parse_command_line()
if command_line_args['mode'] == 'download':
    authenticator = Authenticator(command_line_args['url'])
    downloader = Downloader(authenticator.authenticate())
    downloader.download_encrypted_file()
    downloader.download_encrypted_key()
elif command_line_args['mode'] == 'download->decrypt':
    authenticator = Authenticator(command_line_args['url'])
    downloader = Downloader(authenticator.authenticate())
    downloader.download_encrypted_file()
    downloader.download_encrypted_key()
    cryptographer = Cryptographer()
    cryptographer.decrypt_symmetric_key()
