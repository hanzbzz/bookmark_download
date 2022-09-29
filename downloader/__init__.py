
import os

from flask import Flask, render_template, session
from . import auth, api

def create_app():
    app = Flask(__name__,static_url_path="/static")
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        
        logged_in = session.get('access_token') is not None
        username, profile_pic_url = session.get('username'), session.get('profile_pic_url')
        return render_template('index.html', logged_in=logged_in, username=username, profile_pic_url=profile_pic_url)

    app.register_blueprint(auth.bp)
    app.register_blueprint(api.bp)

    app.permanent_session_lifetime = 60 * 60 * 24 
    @app.before_request
    def permanent_session():
        session.permanent = True
    
    return app