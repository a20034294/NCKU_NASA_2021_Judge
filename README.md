# CCNSAnime_ffmpeg_pool

## Dependencies
* pipenv
```pip3 install pipenv```
* redis
* ffmpeg

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