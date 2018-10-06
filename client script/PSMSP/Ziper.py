import os
import shutil
import sys

class Ziper:

    def zip_security_files(self):
        if os.path.exists('user/secFiles/') and not len(os.listdir('user/secFiles/')) == 0:
            shutil.make_archive('ziped', 'zip', 'user/secFiles')
        else:
            print("The directory with security files does not exist or is empty.")
            sys.exit(1)

    def unzip_security_files(self):
        shutil.unpack_archive('ziped.zip', 'user/secFiles', 'zip')
        os.remove("ziped.zip")