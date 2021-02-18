import json
import clipboard
import sys

class Passworder:

    def __init__(self, json_string):
        self.json_string = json_string

    def get_password(self, name):
        json_dict = json.loads(self.json_string)
        try:
            clipboard.copy(json_dict[name])
        except Exception as e:
            print(e)
            sys.exit(1)

json_string = '{"google": "google pass", "microsoft": "mic pass"}'

json_obj = json.loads(json_string)
json_obj['amazon'] = 'amazon pass'

j = json.dumps(json_obj)

print(j.encode('utf-8'))
