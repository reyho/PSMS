'''
This script is for test purpose only.
With it I can test if the session is working.
This script starts only the session, and with the other script
(other_session_test.py) I check if the session is maintained.
(Ofcourse it's not)
'''

#Importing the Authenticator class
from PSMSP.Authenticator import Authenticator

#Prompting the user to enter the url of the server
url = input('Enter the url: ')


authenticator = Authenticator(url)
authenticator.get_ciphertext()
authenticator.load_priv_key()
decrypted_message = authenticator.decrypt_message()

print(decrypted_message)



