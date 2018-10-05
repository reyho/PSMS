'''
The working python script
'''

#Importing the Authenticator and Downloader class
from PSMSP.Authenticator import Authenticator
from PSMSP.Downloader import Downloader
from PSMSP.Parser import Parser
from PSMSP.Cryptographer import Cryptographer
from PSMSP.Ziper import Ziper

cryptographer = Cryptographer()
parser = Parser()
command_line_args = parser.parse_command_line()

if command_line_args['mode'] == 'encrypt_sec_files':
    ziper = Ziper()
    ziper.zip_security_files()
    cryptographer.decrypt_symmetric_key(command_line_args['path'])
    cryptographer.encrypt_file()
elif command_line_args['mode'] == 'decrypt_symm_key':
    cryptographer.decrypt_symmetric_key(command_line_args['path'], materialize=True)
elif command_line_args['mode'] == 'encrypt_symm_key':
    cryptographer.encrypt_symmetric_key(command_line_args['path'])
elif command_line_args['mode'] == 'decrypt_sec_files':
    ziper = Ziper()
    cryptographer.decrypt_symmetric_key(command_line_args['path'])
    cryptographer.decrypt_file()
    ziper.unzip_security_files()
    
    