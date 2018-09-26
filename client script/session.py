'''
The working python script
'''

#Importing the Authenticator class
from PSMSP.Authenticator import Authenticator

#Prompting the user to enter the url of the server
url = input('Enter the url: ')


authenticator = Authenticator(url)
authenticator.get_ciphertext()
authenticator.load_priv_key()
decrypted_message = authenticator.decrypt_message()

url2 = 'http://localhost/PSMS/sesija1.php'

authenticator.validate_message(url2, decrypted_message)
