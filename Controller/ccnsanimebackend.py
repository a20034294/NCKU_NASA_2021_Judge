import requests
from os import getenv as env


def auth_request(uri, method, payload=None):
    url = env('CCNS_ANIME_BACKEND_URL') + '/token/'
    data = dict()
    data['username'] = env('CCNS_ANIME_BACKEND_USER')
    data['password'] = env('CCNS_ANIME_BACKEND_PASSWORD')
    result = requests.post(url, json=data)
    token = result.json()['access']

    url = env('CCNS_ANIME_BACKEND_URL') + uri
    headers = {"Authorization": f"Bearer {token}"}

    print(url)
    if method == 'GET':
        r = requests.get(url=url, json=payload, headers=headers)
        print(r.status_code)
        return r

    if method == 'POST':
        r = requests.post(url=url, json=payload, headers=headers)
        print(r.status_code)
        return r


def create_anime(
    title: str,
    description: str = '',
    source: str = '未知',
    finished: str = '連載中'
):
    uri = '/anime/'
    data = {
        "title": title,
        "description": description,
        "source": source,
        "finished": finished
    }
    import json
    print(json.dumps(data))
    print(auth_request(uri, 'POST', data).json())
    return


def create_anime_episode(
    anime_id: str,
    episode: str,
    video_path: str,
    ass_path: str,
    resolution: str
):
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
