# -*- coding: utf-8 -*-
import os.path
import zipfile
from datetime import datetime
from time import time

from flask import request, render_template
from flask_uploads import UploadSet, ALL, configure_uploads, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from configparser import ConfigParser
import data_handle_model.csv_handle
from control.event_manger import *
##app = create_flask_app()

from make_celery import app
basedir = data_handle_model.handle.get_current_parentpath()
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_PRIVATE_DEST'] = basedir + '/data/test/tmp'
zip_exract=basedir+'/data/test/'
ALLOWED_EXTENSIONS = {'txt', 'jpg', 'json', 'csv','zip'}
private=UploadSet('private',ALL)
configure_uploads(app,private)
patch_request_class(app)

print(app.template_folder)
class UploadForm(FlaskForm):
    file = FileField(validators=[FileAllowed(private, 'Plaease input IMAGE or DOCUMENT or TEXT!'), FileRequired('File was empty!')])
    submit = SubmitField('Upload')

@app.route('/',methods=['GET','POST'])
def upload_file():

    form=UploadForm()
    if request.method == 'POST':
        # files = request.files.getlist(['file'])
        # for file in files:
        """
        todo 多文件上传，还有如何判断哪些文件是一个执行任务 
        目前 必须提前压缩打包
        """
        file =request.files['file']
        if file and allowed_file(file.filename):
            filename = private.save(form.file.data)
            type_check=True
            file_url=app.config['UPLOADED_PRIVATE_DEST']+'/'+filename
            file_url = file_url.replace('\\', '/')
            start_handle_csv(file_url,zip_exract)
        else:
            type_check=False
            file_url="please input particular file, now we can only support zip"
        return render_template('file.html',form=form,file_url=file_url,type_check=type_check)
    if request.method =='GET':
        return render_template('file.html',form=form,file_url=None,type_check=False)


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
    importer()
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
    importer()
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

@app.route('/hello')
def hello():
    return 'hello world!'

@app.route('/time',methods=["GET","POST"])
def get_time():
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

from control.task import test
@app.route('/async_test',methods=["GET","POST"])
def submit():
    start_time=time()
    test.delay()
    cost=time()-start_time
    return cost

if __name__ == "__main__":
    start()
