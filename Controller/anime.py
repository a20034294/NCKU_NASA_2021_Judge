from flask import jsonify, request, Response
from tasks import anime_create, celery
from celery.result import AsyncResult
import os
from os import getenv as env
import re
"""
{
    "src_path": "aaa/src/ccc.mp4",
    "dst_path": "aaa/stream",
    "token": "123456"
}
"""


def create():
    data = request.get_json(silent=True)
    if data is None:
        return Response('{"message": "application/json needed"}',
                        status=406, mimetype='application/json',)

    data['src_path'], dangerous_cnt = re.subn(
        '([*|\"\\\']|\.\.\\/)', '', data['src_path'])
    if dangerous_cnt > 0:
        return Response('{"message": "操你媽給我滾喔"}',
                        status=400, mimetype='application/json')

    dir, extension = os.path.splitext(data['src_path'])
    if extension != '.mp4':
        return Response('{"message": "Only support .mp4"}',
                        status=501, mimetype='application/json')

    data['dst_path'], dangerous_cnt = re.subn(
        '([*|\"\\\']|\.\.\\/)', '', data['dst_path'])
    if dangerous_cnt > 0:
        return Response('{"message": "操你媽給我滾喔"}',
                        status=400, mimetype='application/json')

    data['src_path'] = data['src_path'].lstrip('/')
    data['dst_path'] = data['dst_path'].lstrip('/')

    resp_data = dict()
    resp_data['task_id'] = anime_create.delay(
        data['src_path'], data['dst_path']).task_id
    return jsonify(resp_data)


def status(task_id):
    task = AsyncResult(task_id, app=celery)

    resp_data = dict()

    resp_data['status'] = dict()
    success = task.ready()
    if success:
        for resolution, sub_task_id in task.get().items():
            sub_task = AsyncResult(sub_task_id, app=celery)

            resp_data['status'][resolution] = sub_task.status
            success &= sub_task.status == 'SUCCESS'

    resp_data['task_id'] = task_id
    resp_data['success'] = success

    return jsonify(resp_data)
