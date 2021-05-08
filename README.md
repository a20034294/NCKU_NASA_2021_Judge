# CCNSAnime_ffmpeg_pool

## Dependencies
* pipenv
`pip3 install pipenv`
* redis
`apt install redis-server`
* ffmpeg
`apt install ffmpeg`

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
### [Create new task](Document/anime_api.md#create-new-task)
### [Get Task status](Document/anime_api.md#get-task-status)
