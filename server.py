# -*- coding: utf-8 -*-

import os
from neo4j import GraphDatabase
import configparser
import json
from flask import jsonify
from app import make_app,make_celery
from celery_task.task import apptask, get_time, utli
from data_handle_model.csv_handle import get_current_parentpath
app=make_app()
# cel=make_celery(app)
from API.test import demo_task
basedir = get_current_parentpath()
#app.config['SECRET_KEY'] = 'I have a dream'
#app.config['UPLOADED_PRIVATE_DEST'] = basedir + '/data/test/tmp'
print(os.getcwd())
print(basedir+'/data/test/tmp')




if __name__=='__main__':


    print(app)
    app.run()
    # # print(app.config)
    # # print(cel.conf)
    # i=demo_task.apply_async((1,2),routing_key='celery', queue='celery')
    #print(i)
    # apptask.delay()
    # get_time.delay()
    #utli.delay()