# Api
[Home](../README.md#api)
## Create new task
* **URL**
    POST `/anime/create`

* **Header**

    | Key | Value | Required |
    | ----| ------| -------- |
    | Content-Type | application/json | **`Required`** |
    | Authorization | PRE-SHARED-TOKEN | **`Required`** |

* **Body Json Params**
    * **src_path `Required`**<br>
        `string`<br>
        Source video path, only mp4 are supported now<br>
    * **dst_path `Optional(use this or anime_id and episode_count)`**<br>
        `string`<br>
        Output stream files destination(.ts, .m3u8), when front-end request https://yourhost/dst_path/playlist.m3u8 should response playlist.m3u8 in your dst_path
    * **anime_id `Optional`**<br>
        `string`<br>
        Anime id of CCNSAnime_Backend, must set env('CCNS_ANIME_BACKEND_ACTIVE'), you need another repo
    * **episode_count `Optional`**<br>
        `string`<br>
        Episode count of CCNSAnime_Backend, must set env('CCNS_ANIME_BACKEND_ACTIVE'), you need another repo

* **Respponse**
    * **task_id**<br>
        `string`<br>
        Task id which can be used to trace this task<br>

* **Example**


    * **Request**
        ```zsh
        curl --location --request POST 'http://127.0.0.1:5000/anime/create' \
        --header 'Authorization: PRE-SHARED-TOKEN' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "src_path": "/root/test/src.mp4",
            "dst_path": "/to/your/output/dir"
        }'
        ```

    * **Respanse**
        Code: `200`

        Body:
        ```json
        {
            "task_id": "02d636f0-bddc-4c40-a389-4c25d103453f"
        }
        ```


## Get task status
* **URL**
    GET `/anime/status/<task_id>`

* **Header**

    | Key | Value | Required |
    | ----| ------| -------- |
    | Authorization | PRE-SHARED-TOKEN | **`Required`** |

* **Url Params**
    * **task_id `Required`**<br>
        `string`<br>
        Task id responsed from /anime/create<br>

* **Respponse**
    * **status**<br>
        `dict`<br>
        Tasks status<br>
        * key<br>
            `string`<br>
            resolution<br>
        * value<br>
            `string`<br>
            status<br>
            [Celery status](https://docs.celeryproject.org/en/stable/reference/celery.states.html)<br>
    * **success**<br>
        `bool`<br>
        Whole task are success or not<br>


* **Example**


    * **Request**
        ```zsh
        curl --location --request GET 'http://127.0.0.1:5000/anime/status/02d636f0-bddc-4c40-a389-4c25d103453f' \
        --header 'Authorization: PRE-SHARED-TOKEN'
        ```

    * **Respanse**
        Code: `200`

        Body:
        ```json
        {
            "status": {
                "1080p": "STARTED",
                "480p": "PENDING",
                "1080p_uspp": "FAILURE",
                "2160p": "SUCCESS"
            },
            "result": {
                "1080p": {
                    "log": "LOGS HERE",
                    "paraent_task_id": "02d636f0-bddc-4c40-a389-4c25d103453f",
                    "playlist_path": "2/MQ==/playlist_h264_1080p_uspp.m3u8",
                    "resolution": "1080",
                    "status": "FAILURE"
                }
                ...
            },
            "success": false,
            "task_id": "02d636f0-bddc-4c40-a389-4c25d103453f"
        }
        ```