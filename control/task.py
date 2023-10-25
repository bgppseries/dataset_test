import abc
import uuid
import json
from celery import Celery


cel=Celery('task')
cel.config_from_object('config')

#from cel import cel
import time
#import evalute.all
@cel.task
def test():
    print("it is a test func")
    time.sleep(5)
    print("test func has done")

# @cel.task
# def evaluate_begin():
#
#
