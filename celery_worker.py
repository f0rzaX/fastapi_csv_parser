from celery import Celery
from app.parser import parse_and_validate
from dotenv import load_dotenv
import os

load_dotenv()

CELERY_BROKER_URL = os.getenv("REDIS_URL")
celery = Celery("tasks", broker=CELERY_BROKER_URL)


@celery.task
def process_file(file_path):
    parse_and_validate(file_path)
