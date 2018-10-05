import argparse
import os

class Parser:

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--decrypt', action='store_true')
    parser.add_argument('-e', '--encrypt', action='store_true')
    parser.add_argument('--symmkey', action='store_true')

    parser.add_argument('-u', '--url', default='http://localhost/PSMS/download.php')
    parser.add_argument('--upload', action='store_true')

    def __init__(self):
        self.__args = Parser.parser.parse_args()

    def parse_command_line(self):
        if self.__args.encrypt and not self.__args.decrypt and not self.__args.symmkey:
            return dict(
                mode='encrypt_sec_files'
            )
        elif self.__args.decrypt and self.__args.symmkey and not self.__args.encrypt:
            return dict(
                mode='decrypt_symm_key'
            )
        elif self.__args.encrypt and self.__args.symmkey and not self.__args.decrypt:
            return dict(
                mode='encrypt_symm_key'
            )
        elif self.__args.decrypt and not self.__args.encrypt and not self.__args.symmkey:
            return dict(
                mode='decrypt_sec_files'
            )
