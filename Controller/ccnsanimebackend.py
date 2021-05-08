import requests
from os import getenv as env


def auth_request(uri, method, payload):
    url = env('CCNS_AMIME_BACKEND_URL') + '/token/'
    data = dict()
    data['username'] = env('CCNS_AMIME_BACKEND_USER')
    data['password'] = env('CCNS_AMIME_BACKEND_PASSWORD')
    result = requests.post(url, data)
    token = result.json()['access']

    url = env('CCNS_AMIME_BACKEND_URL') + uri
    headers = {"Authorization": f"Bearer {token}"}

    if method == 'GET':
        return requests.get(url=url, data=payload, headers=headers)

    if method == 'POST':
        return requests.post(url=url, data=payload, headers=headers)


def create_anime():
    return


def create_anime_episode(anime_id: str, episode: str, video_path: str, ass_path: str, resolution: str):
    uri = '/anime/' + anime_id + '/episode'
    data = {
        'episode_count': episode,
        'video_path': video_path,
        'ass_path': ass_path,
        'resolution': resolution,
        'encoded': True
    }
    import json
    print(json.dumps(data))
    print(auth_request(uri, 'POST', data).json())
    return
