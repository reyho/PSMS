'''
The working python script
'''

#Importing the Authenticator class
from PSMSP.Authenticator import Authenticator
from PSMSP.Downloader import Downloader

#s = requests.Session()
#Prompting the user to enter the url of the server
url = input('Enter the url: ')


authenticator = Authenticator(url)
downloader = Downloader(authenticator.authenticate())

#url2 = 'http://localhost/PSMS/sesija1.php'

downloader.download_encrypted_file()
#downloader.get_filename_from_cd(downloader.print_cd(url2))
