from flask import jsonify, request, Response
from tasks import anime_create, celery
from celery.result import AsyncResult
import os
from os import getenv as env
import re
import base64
"""
{
    "src_path": "aaa/src/ccc.mp4",
    "dst_path": "aaa/stream",
    "anime_id": "1",
    "episode_count": "1"
}
"""


def create():
    data = request.get_json(silent=True)
    if data is None:
        return Response('{"message": "Json parse error"}',
                        status=406, mimetype='application/json')

    if 'src_path' not in data.keys() or type(data['src_path']) != str:
        return Response('{"message": "src_path not set or not str"}',
                        status=400, mimetype='application/json')

    data['src_path'], dangerous_cnt = re.subn(
        '([*|\"\\\']|\.\.\\/)', '', data['src_path'])
    if dangerous_cnt > 0:
        return Response('{"message": "操你媽給我滾喔"}',
                        status=400, mimetype='application/json')

    dir, extension = os.path.splitext(data['src_path'])
#    if extension != '.mp4':
#        return Response('{"message": "Only support .mp4"}',
#                        status=501, mimetype='application/json')

    if env('CCNS_ANIME_BACKEND_ACTIVE') and 'anime_id' in data.keys() and 'episode_count' in data.keys():
        if type(data['anime_id']) != str:
            return Response('{"message": "anime_id must be str"}',
                            status=400, mimetype='application/json')
        if type(data['episode_count']) != str:
            return Response('{"message": "episode_count must be str"}',
                            status=400, mimetype='application/json')

        data['dst_path'] = data['anime_id'] + '/' + \
            str(base64.urlsafe_b64encode((data['episode_count']).encode('utf-8')))

    if 'dst_path' not in data.keys() or type(data['dst_path']) != str:
        return Response('{"message": "dst_path not set or not str"}',
                        status=400, mimetype='application/json')

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
    resp_data['result'] = dict()
    success = task.ready()
    if success:
        for resolution, sub_task_id in task.get().items():
            sub_task = AsyncResult(sub_task_id, app=celery)
            print(sub_task)

            sub_task_status = sub_task.status
            if sub_task.ready():
                resp_data['result'][resolution] = sub_task.get()
                sub_task_status = resp_data['result'][resolution]['status']

            resp_data['status'][resolution] = sub_task_status
            success &= sub_task_status == 'SUCCESS'

    resp_data['task_id'] = task_id
    resp_data['success'] = success

    return jsonify(resp_data)
