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

private=UploadSet('private',ALL)
ALLOWED_EXTENSIONS = {'txt', 'jpg', 'json', 'csv','zip'}
class UploadForm(FlaskForm):
    file = FileField(validators=[FileAllowed(private, 'Plaease input IMAGE or DOCUMENT or TEXT!'), FileRequired('File was empty!')])
    submit = SubmitField('Upload')

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
def start_handle(path):
    listen= Listener("the info of the server")
    eventloop=EventLoop()
    eventloop.AddEventListener(EVEVT_RECV_FILE_CSV,listen.handel)
    eventloop.Start()
    s=sigmoid(eventloop)
    s.send_signal(path,str(uuid4()))

def start():
    config = ConfigParser()
    config.read('../setting/set.config', encoding='UTF-8')
    info=config['flask']
    addr=info['run_ipaddr']
    port=info['run_port']
    app.run(debug=True,host=addr,port=int(port))


