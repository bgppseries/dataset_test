import time

from celery import shared_task, Celery
from create_bind import create_flask_app
# flask_app=create_flask_app()
# celery_app=flask_app.extensions["celery"]

@shared_task(name='test_work',ignore_result=False)
def test():
    time.sleep(5)
    return "hello world!"
