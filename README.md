# PSMS
Password storing and managing system
I replaced the tab with 4 spaces for my indentation so I wont get the inconsistent use of tabs and spaces error

Command line arguments:
Encrypt security files: "session.py -e --inkey pathToPrivateKey"
Decrypt security files: "session.py -d --inkey pathToPrivateKey"

Decrypt symmetric key: "session.py -d --symmkey --inkey pathToPrivateKey"
Encrypt symmetric key: "session.py -e --symmkey --inkey pathToPrivateKey"