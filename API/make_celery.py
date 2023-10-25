#from create_bind import create_flask_app
from create_bind import create_flask_app

app=create_flask_app()

celery_app=app.extensions["celery"]
