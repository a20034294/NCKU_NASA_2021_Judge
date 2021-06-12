import json
from os import getenv as env
from flask import Response, request
from functools import wraps

token_list = set()
with open(env('STUDENT_PATH'), 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        word = line.split(',')
        token_list.add(word[0] + word[1])
        print(word[0] + word[1])


def token_is_valid(token):
    if token not in token_list:
        return False
    return True


def assert_auth(f):
    @wraps(f)
    def decorated_func(*args, **kws):
        student_id = request.values.get('student_id')
        password = request.values.get('password')
        token = student_id + password
        if token == None or token not in token_list:
            return Response('{"message": "Student id & password not valid"}',
                            status=403, mimetype='application/json')
        return f(*args, **kws)
    return decorated_func
