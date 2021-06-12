from flask import request, Response, jsonify
from tasks import judge_create, celery
from celery.result import AsyncResult
import os
from os import getenv as env
import re


def create():

    dangerous_cnt = 0
    student_id, dangerous_cnt = re.subn(
        '([*|\"\\\']|\.\.\\/)', '', request.values.get('student_id'))
    if dangerous_cnt > 0:
        return Response('{"message": "欸這不是 CTF 欸，快來跟助教道歉"}',
                        status=400, mimetype='application/json')
    password, dangerous_cnt = re.subn(
        '([*|\"\\\']|\.\.\\/)', '', request.values.get('password'))
    if dangerous_cnt > 0:
        return Response('{"message": "欸這不是 CTF 欸，快來跟助教道歉"}',
                        status=400, mimetype='application/json')

    resp_data = dict()
    resp_data['task_id'] = judge_create.delay(
        student_id, password).task_id
    return jsonify(resp_data)


def status(task_id):
    task = AsyncResult(task_id, app=celery)

    resp_data = dict()

    resp_data['status'] = task.status
    if resp_data['status'] == 'SUCCESS':
        resp_data['result'] = task.get()['result']
        resp_data['score'] = task.get()['score']

    return jsonify(resp_data)
