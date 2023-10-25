##  app主体文件
from celery import Celery,Task

from flask import Flask

def create_celery_app(app:Flask)->Celery:
    class FlaskTask(Task):
        def __call__(self, *args:object, **kwargs:object)->object:
            with app.app_context():
                return self.run(*args,**kwargs)
    celery_app=Celery(app.name,task_cls=FlaskTask)
    celery_app.config_from_object('config.celery_config')
    celery_app.set_default()
    app.extensions["celery"]=celery_app#将celery设置为Flask app的扩展
    return celery_app

def create_flask_app()->Flask:
    """
    创建Flask app实例，并创建celery app实例，将二者绑定，通过extension
    :return:返回绑定后的Flask app
    """
    app = Flask(__name__)
    app.config.from_prefixed_env()
    create_celery_app(app)
    return app




# def register_blueprints(app):
#     app.register_blueprint(th, url_prefix='/')
# def register_commands(app):
#     @app.cli.command()
#     @click.option('--drop', is_flag=True, help='Create after drop.')
#     def initdb(drop):
#         """Init databases."""
#         if drop:
#             click.confirm(
#                 'This operation will delete the database, do you want to continue?',
#                 abort=True)
#             db.drop_all()
#             click.echo('Drop tables.')
#         db.create_all()
#         click.echo('Initialized database.')
