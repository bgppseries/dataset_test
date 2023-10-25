# import time
#
# from task import test
#
# if __name__=='__main__':
#
#     r=test.delay()
#     print('task finished?',r.ready())
#     time.sleep(10)
#     print('task may have done:',r.ready())
import time

from celery import Celery
from celery.exceptions import TimeoutError
from celery.result import AsyncResult
from kombu import Queue, Exchange

# celery配置，4.0之后引入了小写配置，这种大写配置在6.0之后将不再支持
# 可以参考此链接
# https://docs.celeryproject.org/en/stable/userguide/configuration.html?highlight=worker#std-setting-enable_utc
CONFIG = {
    # 设置时区
    'celery_timezone': 'Asia/Shanghai',
    # 默认为true，UTC时区
    'celery_enable_utc': False,
    # broker，注意rabbitMQ的VHOST要给你使用的用户加权限
    'broker_url': 'amqp://qwb:784512@192.168.1.121:5672/test',
    # backend配置，注意指定redis数据库
    'result_backend': 'redis://:ningzaichun@192.168.1.121:6379/1',
    'broker_connection_retry_on_startup' : True

}
app = Celery()
app.config_from_object(CONFIG)


@app.task(name='demo_task')
def demo_task(x, y):
    print(f"这是一个demo任务，睡了10秒，并返回了{x}+{y}的结果。")
    time.sleep(10)
    return x + y


def call():
    def get_result(task_id):
        res = AsyncResult(task_id)
        try:
            # 拿到异步任务的结果，需要用task_id实例化AsyncResult，再调用get方法，get默认是阻塞方法，提供timeout参数，此处设置为0.1秒
            res.get(0.1)
            return res.get(0.1)
        except TimeoutError:
            return None

    tasks = []
    print("开始下发11个任务")
    for _ in range(11):
        tasks.append(demo_task.apply_async((_, _), routing_key='celery', queue='celery'))
        print('1')
    print("等待10秒后查询结果")
    time.sleep(10)
    for index, task in enumerate(tasks):
        task_result = get_result(task.id)
        if task_result is not None:
            print(f"任务{index}的返回值是：{task_result}")
        else:
            print(f"任务{index}还没执行结束")
    print("再等待10秒")
    time.sleep(10)
    print(f"任务10的返回值是：{get_result(tasks[-1].id)}")


if __name__ == '__main__':
    call()
