# CCNSAnime_ffmpeg_pool

## Dependencies
* pipenv
`pip3 install pipenv`
* redis
* ffmpeg
`pip3 install ffmpeg`

## Before start
`cp .env.template .env`
then edit as needed
## Usage
Need to run 2 program
```bash
pipenv install

pipenv run flask run
&
pipenv run celery -A tasks worker -c 1 -l info
```

## Api
### Create new task
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
    * **dst_path `Required`**<br>
        `string`<br>
        Output stream files destination(.ts, .m3u8), when front-end request https://yourhost/dst_path/playlist.m3u8 should response playlist.m3u8 in your dst_path

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