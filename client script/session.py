'''
The working python script
'''

#Importing the Authenticator and Downloader class
from PSMSP.Authenticator import Authenticator
from PSMSP.Downloader import Downloader
from PSMSP.Parser import Parser
from PSMSP.Cryptographer import Cryptographer
from PSMSP.Ziper import Ziper
from PSMSP.Generator import Generator
from PSMSP.Uploader import Uploader
import configparser
import os

#Checking if the required directorys exist. If not, then create them
if not os.path.exists('../keys'):
    os.mkdir('../keys')
if not os.path.exists('user/'):
    os.mkdir('user/')
if not os.path.exists('user/encFile/'):
    os.mkdir('user/encFile/')
if not os.path.exists('user/secFiles/'):
    os.mkdir('user/secFiles/')
if not os.path.exists('user/symmKey/'):
    os.mkdir('user/symmKey/')
if not os.path.exists('user/pass/'):
    os.mkdir('user/pass/')

cryptographer = Cryptographer()
parser = Parser()
config = configparser.ConfigParser()
config.read('config.ini')
command_line_args = parser.parse_command_line()

if command_line_args['mode'] == 'encrypt_sec_files':
    ziper = Ziper()
    ziper.zip_security_files()
    cryptographer.encrypt_file(config['Paths']['PrivateKey'])

elif command_line_args['mode'] == 'decrypt_symm_key':
    cryptographer.decrypt_symmetric_key(config['Paths']['PrivateKey'], materialize=True)

elif command_line_args['mode'] == 'encrypt_symm_key':
    cryptographer.encrypt_symmetric_key(config['Paths']['PrivateKey'], 'user/symmKey/aes_key.key')

elif command_line_args['mode'] == 'decrypt_sec_files':
    ziper = Ziper()
    cryptographer.decrypt_file(config['Paths']['PrivateKey'])
    ziper.unzip_security_files()

elif command_line_args['mode'] == 'download_enc_file_symmkey':
    authenticator = Authenticator(config['Paths']['ServerURL'], config['Paths']['Serverkeypath'])
    authenticate_dict = authenticator.authenticate()
    downloader = Downloader(authenticate_dict)
    downloader.download()

elif command_line_args['mode'] == 'download_enc_file':
    authenticator = Authenticator(config['Paths']['ServerURL'], config['Paths']['Serverkeypath'])
    authenticate_dict = authenticator.authenticate()
    downloader = Downloader(authenticate_dict)
    downloader.download_encrypted_file()

elif command_line_args['mode'] == 'generate_key_pair':
    generator = Generator()
    generator.generate_key_pair('../keys/')

elif command_line_args['mode'] == 'generate_aes_key':
    generator = Generator()
    generator.generate_aes_key('../keys/')

elif command_line_args['mode'] == 'upload_file':
    authenticator = Authenticator(config['Paths']['ServerURL'], config['Paths']['Serverkeypath'])
    uploader = Uploader(authenticator.authenticate())
    uploader.upload_encrypted_file()

elif command_line_args['mode'] == 'upload_key':
    authenticator = Authenticator(config['Paths']['ServerURL'], config['Paths']['Serverkeypath'])
    uploader = Uploader(authenticator.authenticate())
    uploader.upload_encrypted_key()
