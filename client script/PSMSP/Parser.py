import argparse
import os

class Parser:

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--decrypt', action='store_true')
    parser.add_argument('-e', '--encrypt', action='store_true')
    parser.add_argument('-u', '--url', default='http://localhost/PSMS/download.php')
    parser.add_argument('--upload', action='store_true')

    def __init__(self):
        self.__args = Parser.parser.parse_args()

    def parse_command_line(self):
        if not self.__args.upload and self.__args.decrypt:
            return dict(
                mode='download->decrypt',
                url=self.__args.url
            )
        elif not self.__args.upload and not self.__args.decrypt:
            return dict(
                mode='download',
                url=self.__args.url
            )
        elif self.__args.upload and self.__args.encrypt:
            return dict(
                mode='encrypt->upload',
                url=self.__args.url
            )
        elif self.__args.upload and not self.__args.encrypt:
            return dict(
                mode='upload',
                url=self.__args.url
            )


    def __make_new_user(self):
        while True:
            user_name = input('Choose your user name (q=quit): ')
            if user_name.lower() == 'q':
                return -1
            elif os.path.exists(user_name):
                print('That user name already exists.')
            else:
                print('Creating user: ' + user_name)
                user_path = os.path.join('users', user_name)
                os.makedirs(user_path)
                os.makedirs(os.path.join(user_path, 'key'))
                os.makedirs(os.path.join(user_path, 'efile'))
                os.makedirs(os.path.join(user_path, 'defile'))
                return user_name
