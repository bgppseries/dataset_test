from app import make_app,make_celery
from celery_task.task import apptask,get_time
app=make_app()
# cel=make_celery(app)
from API.test import demo_task


if __name__=='__main__':
    print("hello")
    app.run()
    # # print(app.config)
    # # print(cel.conf)
    # i=demo_task.apply_async((1,2),routing_key='celery', queue='celery')
    # print(i)