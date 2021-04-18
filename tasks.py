from Task.anime_create import *
from celery import Celery
import time
from os import getenv as env
from dotenv import load_dotenv
load_dotenv()

celery = Celery(
    'tasks',
    broker=env('CELERY_BROKER'),
    backend=env('CELERY_BACKEND'),
)


@celery.task
def anime_create(src_path, dst_path):
    return anime_create_task(src_path, dst_path)
