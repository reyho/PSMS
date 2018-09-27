'''
This script is for test purpose only.
With it I can test if the session is working.
With this script i check if the session to the server
is maintained.
'''

#Importing the Authenticator class
from PSMSP.Authenticator import Authenticator

url = 'Some string'

authenticator = Authenticator(url)

#Prompting the user to enter the decrypted message of the server
decrypted_message = input('Enter the decrypted message: ')

url2 = 'http://localhost/PSMS/sesija1.php'

authenticator.validate_message(url2, decrypted_message)