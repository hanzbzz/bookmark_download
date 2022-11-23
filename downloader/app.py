import os

from flask import Flask, render_template, session, g
from . import auth, api
from . import init_db, db

def create_app():
    app = Flask(__name__,static_url_path="/static")
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    init_db.init()

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        logged_in = session.get('bearer_token') is not None
        return render_template('user.html', logged_in=True) if logged_in else render_template('login.html', logged_in=False)

    app.register_blueprint(auth.bp)
    app.register_blueprint(api.bp)

    app.permanent_session_lifetime = 60 * 60 * 24 
    @app.before_request
    def permanent_session():
        g.username, g.profile_pic_url = session.get('username'), session.get('profile_pic_url')
        g.conn = db.get_db_connection()
        session.permanent = True
    

    return app