import os
from dotenv import load_dotenv
import tweepy
from flask import session, Blueprint, redirect, url_for, send_file, request, abort
import shutil
from . import utils


load_dotenv()

api_key = os.environ["API_KEY"]
api_secret = os.environ["API_SECRET"]

bp = Blueprint('api', __name__, url_prefix="/api")

client = tweepy.Client(consumer_key=api_key, consumer_secret=api_secret)

@bp.before_request
def client_init():
    bearer_token = session.get('bearer_token')
    client.bearer_token = bearer_token

@bp.route('/user')
def user():
    try:
        user: tweepy.User = client.get_me(user_fields='profile_image_url', user_auth=False).data
    except tweepy.errors.Forbidden:
        abort(403)
        
    session['username'] = user.username
    session['profile_pic_url'] = user.profile_image_url
    return redirect(url_for('index'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.route('/download')
def download():
    try:
        bookmarks = client.get_bookmarks(expansions=['attachments.media_keys'],media_fields=["url","variants"])
    except (TypeError, tweepy.errors.Forbidden):
        abort(403)
    tweets = bookmarks.data
    media = bookmarks.includes.get('media')
    if tweets is None:
        return "Your bookmarks are empty"
    tweets = utils.parse_bookmarks(tweets, media)
    selected_types = list(request.args.keys())
    include = request.args.get("include") is not None
    print(include)
    path = utils.download_tweets(tweets, selected_types , include)
    zip_file = shutil.make_archive(path, "zip", path)
    resp = send_file(zip_file)
    utils.cleanup(path)

    return resp