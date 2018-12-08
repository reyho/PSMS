import argparse
import os

class Parser:

    parser = argparse.ArgumentParser()
    parser.add_argument('actions', choices=['download', 'upload', 'noload', 'generate'])
    parser.add_argument('-de', choices=['d', 'e',])
    parser.add_argument('--symmkey', action='store_true')

    def __init__(self):
        self.__args = Parser.parser.parse_args()

    def parse_command_line(self):
        if self.__args.actions == 'noload' and self.__args.de == 'e' and not self.__args.symmkey:
            return dict(
                mode='encrypt_sec_files'
            )
        elif self.__args.actions == 'noload' and self.__args.de == 'd' and self.__args.symmkey:
            return dict(
                mode='decrypt_symm_key'
            )
        elif self.__args.actions == 'noload' and self.__args.de == 'e' and self.__args.symmkey:
            return dict(
                mode='encrypt_symm_key'
            )
        elif self.__args.actions == 'noload' and self.__args.de == 'd' and not self.__args.symmkey:
            return dict(
                mode='decrypt_sec_files'
            )
        elif self.__args.actions == 'download' and not self.__args.de:
            return dict(
                mode='download_enc_file'
            )
        elif self.__args.actions == 'generate':
            return dict(
                mode='generate_key_pair'
            )
