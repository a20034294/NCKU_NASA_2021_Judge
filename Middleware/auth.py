import json
from os import getenv as env
from flask import Response, request
from functools import wraps

token_list = set()
for token in json.loads(env('AUTHORIZED_TOKENS')):
    token_list.add(token)


def token_is_valid(token):
    if token not in token_list:
        return False
    return True


def assert_auth(f):
    @wraps(f)
    def decorated_func(*args, **kws):
        data = request.get_json()
        if data is None:
            return Response('{"message": "application/json needed"}',
                            status=406, mimetype='application/json')

        if 'token' not in data.keys() or data['token'] not in token_list:
            return Response('{"message": "Auth token not valid"}',
                            status=403, mimetype='application/json')
        return f(*args, **kws)
    return decorated_func
