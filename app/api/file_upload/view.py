from flask import request

from . import api_file
from .module import UploadForm, allowed_file, private


@api_file.route('/',methods=['GET','POST'])
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

@api_file.route('/hello')
def hello():
    return 'hello world!'

@api_file.route('/time',methods=["GET","POST"])
def get_time():
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

