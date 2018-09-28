'''
The working python script
'''

#Importing the Authenticator and Downloader class
from PSMSP.Authenticator import Authenticator
from PSMSP.Downloader import Downloader


#Prompting the user to enter the url of the server
url = input('Enter the url: ')


authenticator = Authenticator(url)
downloader = Downloader(authenticator.authenticate())
downloader.download_encrypted_file()

