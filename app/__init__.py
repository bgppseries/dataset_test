import os
import click
from flask import Flask,jsonify
from celery import Celery

from app.config.flask_config import config
from app.config import celery_config

from app.api.test import api_test


def make_celery(app):
    #导入Flask配置文件env
    #notice: install python-dotenv
    from dotenv import load_dotenv,find_dotenv
    load_dotenv(find_dotenv())

    celery=Celery(
        app.import_name,
        broker_url="amqp://qwb:784512@192.168.1.121:5672/test",
        result_backend = 'redis://:ningzaichun@192.168.1.121:6379/1'
    )
    # celery.conf.update(app.config)
    celery.config_from_object(celery_config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_contexe():
                return self.run(*args,**kwargs)

    celery.Task=ContextTask
    return celery
def make_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV','development')

    app=Flask('app')
    app.config.from_object(config[config_name])
    register_errors(app)

    register_blueprints(app)
    return app

# def register_extensions(app):
#     from test_api.extensions import db
#     db.init_app(app)
# #    celery_ext.init_app(app)

def register_blueprints(app):
    with app.app_context():

        app.register_blueprint(api_test, url_prefix='/api/test')


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        response = jsonify(code=400, message="Bad Request")
        response.status_code = 400
        return response

    @app.errorhandler(403)
    def forbidden(e):
        response = jsonify(code=403, message="Forbidden")
        response.status_code = 403
        return response

    @app.errorhandler(404)
    def page_not_found(e):
        response = jsonify(code=404, message="The requested URL was not found on the server.")
        response.status_code = 404
        return response

    @app.errorhandler(405)
    def method_not_allowed(e):
        response = jsonify(code=405, message='The method is not allowed for the requested URL.')
        response.status_code = 405
        return response
