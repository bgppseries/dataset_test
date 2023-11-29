# -*- coding: utf-8 -*-
import os.path
import zipfile
from time import time
from uuid import uuid4

from flask_uploads import UploadSet, ALL
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from configparser import ConfigParser
import data_handle_model.csv_handle

ALLOWED_EXTENSIONS = {'txt', 'jpg', 'json', 'csv','zip','html'}
##ALLOWED_EXTENSIONS在allowed_file函数中用到

def allowed_file(filename):
    """
            判断上传的文件是否合法
            :param filename:文件名
            :return: bool
    """
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
def start_handle_csv(path,to):
    data_handle_model.handle.read_csv(path, to)
    print("handle csv success")
    #todo log
    os.remove(path)
    data_handle_model.importer()

def start_handle_zip(path_from,path_to):
    """
    将zip文件解压到指定目录
    todo 指定目录是写死的
    :param path:zip文件目录
    :return:
    """
    with zipfile.ZipFile(path_from,'r') as zip:
        zip.extractall(path_to)
    os.remove(path_from)
    data_handle_model.importer()
def start_handle(filename,path):
    file_type=filename.resplit('.',1)[1]
    config=ConfigParser()
    config.read('./setting/set')
    info=config['flask']
    to=info['to']
    if file_type=='csv':
        start_handle_csv(filename,path)
    elif file_type=='json':
        apoc_json(filename)

def apoc_json(file):
    sql=''



if __name__=='__main__':
    apoc_json('json')



