import shutil
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import requests
import base64


url = input('Enter the url: ')





dec_resp = 1


with open("private_key.pem", "rb") as key_file:

	private_key = serialization.load_pem_private_key(
		key_file.read(),
		password=None,
		backend=default_backend()
	)
	dec_resp = private_key.decrypt(
		ciphertext,
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA1()),
			algorithm=hashes.SHA1(),
			label=None
		)
	)

	print(dec_resp)


url2 = 'http://localhost/nesto/sesija1.php'
response2 = s.get(url2, params={'value': dec_resp}, stream=True)
print(response2.text)
del response2
