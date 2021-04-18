import json
from os import getenv as env


token_list = set()
for token in json.loads(env('AUTHORIZED_TOKENS')):
    token_list.add(token)


def token_is_valid(token):
    if token not in token_list:
        return False
    return True
