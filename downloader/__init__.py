
import os

from flask import Flask, render_template
from . import auth

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return render_template('base.html')

    app.register_blueprint(auth.bp)
    return app