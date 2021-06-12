from Task.judge_create import judge_create_task
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
def judge_create(self, student_id, password):
    return judge_create_task(student_id, password)
