import os
from dotenv import load_dotenv
import tweepy
from flask import session, Blueprint, redirect, url_for

load_dotenv()

api_key = os.environ["API_KEY"]
api_secret = os.environ["API_SECRET"]

bp = Blueprint('api', __name__, url_prefix="/api")

client = tweepy.Client(consumer_key=api_key,
    consumer_secret=api_secret)

@bp.before_request
def client_init():
    access_token = session.get('access_token')
    access_secret = session.get('access_secret')
    client.access_token, client.access_token_secret = access_token, access_secret

    
@bp.route('/user')
def user():
    user: tweepy.User = client.get_me(user_fields='profile_image_url').data
    session['username'] = user.username
    session['profile_pic_url'] = user.profile_image_url
    return redirect(url_for('index'))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))