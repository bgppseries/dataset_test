import pandas as pd
from flask import Flask,Blueprint


def handle():
    data=pd.io.stata.read_stata('unhandle_data/Health_History.dta')
    data.to_csv('data/Health_History.csv')

    from flask import Flask, Blueprint, render_template

app = Flask(__name__)
bp = Blueprint('main', __name__, url_prefix='/main')

@bp.route('/')
def home():
    return "hello"

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run()