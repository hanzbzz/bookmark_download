from flask import Blueprint, request, session, redirect, url_for, abort
from dotenv import load_dotenv
import tweepy
import os

load_dotenv()

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]

import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

bp = Blueprint('auth', __name__, url_prefix='/auth')
oauth2 = tweepy.OAuth2UserHandler(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="http://127.0.0.1:8080/auth/callback",
    scope=["tweet.read", "users.read", "bookmark.read"])



@bp.route('/url')
def url():
    auth_url = oauth2.get_authorization_url()
    return redirect(auth_url)

@bp.route('/callback')
def callback():
    try:
        access_token = oauth2.fetch_token(request.url)
    except Exception:
        abort(400)
    session['bearer_token'] = access_token['access_token']
    return redirect(url_for('api.user'))