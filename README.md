# PSMS
Password storing and managing system

The main purpose of this application is to safely store and manage your passwords
and files that you want to keep safe from others.

The way it works is that you have a server who is hosting your encrypted files
so that it is accessible from all places. You authenticate yourself to the server
via private/public key pair and than download the encrypted files. Once downloaded
you decrypt your files. You can access your passwords in the text files, access
other files that are important to you. You can change them and when you are done
with them, you can either encrypt and upload them if you have made some changes
or you can just delete them so they are not on your local system.

In the folder 'client side' you have the python files which are executed on the
clients computer, with whom you are going to download/upload your encrypted files
and encrypt/decrypt them once they are downloaded.
First you need to have a configuration file in the 'client side' folder (you can
see the name in the session.py file or change it to what ever name you want).
The content of the configuration file has to be like follows:
[Paths]
PrivateKey = /path/to/Privatekey/privatekey.pem <!-- The private key for encryption/decryption of your files -->
ServerURL = https://hostname.of/yourPHPscript/download.php
Serverkeypath = /path/to/serverAuthentication/Privatekey/ <!-- The private key used for authentication to download the files -->
