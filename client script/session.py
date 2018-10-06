'''
The working python script
'''

#Importing the Authenticator and Downloader class
from PSMSP.Authenticator import Authenticator
from PSMSP.Downloader import Downloader
from PSMSP.Parser import Parser
from PSMSP.Cryptographer import Cryptographer
from PSMSP.Ziper import Ziper
import configparser
import os

#Checking if the required directorys exist. If not, then create them
if not os.path.exists('user/encFile/'):
    os.mkdir('user/encFile/')
if not os.path.exists('user/secFiles/'):
    os.mkdir('user/secFiles/')
if not os.path.exists('user/symmKey/'):
    os.mkdir('user/symmKey/')

cryptographer = Cryptographer()
parser = Parser()
config = configparser.ConfigParser()
config.read('config.ini')
command_line_args = parser.parse_command_line()

if command_line_args['mode'] == 'encrypt_sec_files':
    ziper = Ziper()
    ziper.zip_security_files()
    cryptographer.decrypt_symmetric_key(config['Paths']['PrivateKey'])
    cryptographer.encrypt_file()
elif command_line_args['mode'] == 'decrypt_symm_key':
    cryptographer.decrypt_symmetric_key(config['Paths']['PrivateKey'], materialize=True)
elif command_line_args['mode'] == 'encrypt_symm_key':
    cryptographer.encrypt_symmetric_key(config['Paths']['PrivateKey'])
elif command_line_args['mode'] == 'decrypt_sec_files':
    ziper = Ziper()
    cryptographer.decrypt_symmetric_key(config['Paths']['PrivateKey'])
    cryptographer.decrypt_file()
    ziper.unzip_security_files()
elif command_line_args['mode'] == 'download_enc_file':
    authenticator = Authenticator(config['Paths']['ServerURL'])
    downloader = Downloader(authenticator.authenticate())
    downloader.download_encrypted_key()
    downloader.download_encrypted_file()
