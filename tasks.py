from Task.anime_create import anime_create_task
from Task.ffmpeg_trans_hls import ffmpeg_trans_hls_task
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
celery.conf.update(task_track_started=True)


@celery.task(bind=True)
def anime_create(self, src_path, dst_path):
    return anime_create_task(src_path, dst_path, self.request.id)


@celery.task
def ffmpeg_trans_hls(src_path, dst_path, resolution, paraent_task_id):
    return ffmpeg_trans_hls_task(src_path, dst_path, resolution, paraent_task_id)
