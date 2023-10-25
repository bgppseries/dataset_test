import time
import os
from flask import current_app
from celery import Task, Celery
from . import config

celery=Celery()
celery.config_from_object(config)

class MyTask(Task): # celery 基类

    def on_success(self, retval, task_id, args, kwargs):
        # 执行成功的操作
        #todo logger
        print('MyTasks 基类回调，任务执行成功')
        return super(MyTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # 执行失败的操作
        # 任务执行失败，可以调用接口进行失败报警等操作
        #todo logger
        print('MyTasks 基类回调，任务执行失败')
        return super(MyTask, self).on_failure(exc, task_id, args, kwargs, einfo)



@celery.task(bind=True, base=MyTask)
def apptask(self):
    print(current_app.config)
    print("==============%s " % current_app.config["SQLALCHEMY_DATABASE_URI"])
    print("++++++++++++++%s " % os.getenv("DATABASE_URL"))
    time.sleep(5)
    return 'success'

@celery.task(bind=True,base=MyTask)
def get_time(self):
    print(time.time())
    time.sleep(5)
    return 'it is a great step'