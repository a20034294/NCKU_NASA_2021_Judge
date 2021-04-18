from flask import jsonify, request, Response
from tasks import anime_create
from auth import token_is_valid
import os
import re
"""
{
    "src_path": "aaa/src/ccc.mp4",
    "dst_path": "aaa/stream",
    "token": "123456"
}
"""


def create():
    data = request.get_json()
    if data == None:
        return Response('{"message": "application/json needed"}',
                        status=406, mimetype='application/json')

    if not token_is_valid(data['token']):
        return Response('{"message": "Auth token not valid"}',
                        status=403, mimetype='application/json')

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

    resp_data = dict()
    resp_data['task_id'] = anime_create.delay(
        data['src_path'], data['dst_path']).task_id
    return jsonify(resp_data)
