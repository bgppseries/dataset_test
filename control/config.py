#coding:utf-8
from datetime import timedelta
from celery.schedules import crontab
# 消息代理使用RabbitMQ。与Celery实例化时broker参数意义相同
broker_url = "amqp://qwb:784512@192.168.1.121:5672/test"

# 结果存储使用redis(默认数据库-零)。与Celery实例化时backend参数意义相同
result_backend = 'redis://192.168.1.121:6379/1'

# LOG配置
worker_log_format = "[%(asctime)s] [%(levelname)s] %(message)s"

# Celery指定时区，默认UTC
timezone = "Asia/Shanghai"

# 任务注册到Celery，采用绝对路径。与Celery实例化时
imports = ("task", )

# 配置，开启进程程序(命令见下文)，任务会被按时读取并发送到指定队列
beat_schedule = {
    "add-erery-30-seconds": {
        "task": "task.add",  # 也可以用别名，绝对路径
        "schedule": timedelta(seconds=30),  # 每 30 秒执行一次
        # "schedule": crontab(hour=9, minute=50),  # 每天早上 9 点 50 分执行一次
        "args": (3, 4)
    }
}
# 此处注意，元组中只有一个值的话，需要最后加逗号
# CELERY_QUEUES={
# }