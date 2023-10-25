from celery import Celery


cel=Celery('task')
cel.config_from_object('config')


# 任务注册

"""绝对路径
方式一:导包
import task

方式二:调接口,切记指向包名，函数autodiscover_tasks会自动找包内的task任务文件(任务文件task在package包内，很明显这里没有包，不能使用)
app.autodiscover_tasks(["xxx.task", ])

方式三：配置文件config引入，本项目使用
"""

if __name__=='__main__':
    cel.start()