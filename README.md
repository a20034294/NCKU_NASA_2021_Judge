# CCNSAnime_ffmpeg_pool

## Dependencies
* pipenv
```pip3 install pipenv```
* redis
* ffmpeg
```pip3 install ffmpeg```

## Before start
```cp .env.template .env``
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

* **Body Json Params**
    * **src_path `Required`**
        `string`
        Source video path, only mp4 are supported now
    * **dst_path `Required`**
        `string`
        Output stream files destination
    * **token `Required`**
        `string`
        Authorize token

* **Respponse**
    * **task_id**
        `string`
        Task id which can be used to trace this task

* **Example**


    * **Request**
        ```bash
        curl --location --request POST 'http://127.0.0.1:5000/anime/create' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "src_path": "/root/test/src.mp4",
            "dst_path": "/root/test/celeryoutput",
            "token": "223445678"
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