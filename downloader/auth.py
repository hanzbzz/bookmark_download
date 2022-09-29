from flask import Blueprint, request, session, redirect, url_for
from dotenv import load_dotenv
import tweepy
import os
import requests


load_dotenv()

api_key = os.environ["API_KEY"]
api_secret = os.environ["API_SECRET"]



bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/url')
def url():
    oauth = tweepy.OAuth1UserHandler(api_key, api_secret, callback="http://localhost:5000/auth/callback")
    auth_url = oauth.get_authorization_url()
    session.clear()
    session["request_token"] = oauth.request_token
    return redirect(auth_url)

@bp.route('/callback')
def callback():
    verifier = request.args.get("oauth_verifier")
    oauth = tweepy.OAuth1UserHandler(api_key, api_secret)
    token = session.get("request_token")
    oauth.request_token = token
    try:
        oauth.get_access_token(verifier)
    except tweepy.TweepyException:
        print("Error trying to get access token")
    session['access_token'] = oauth.access_token
    session['access_secret'] = oauth.access_token_secret
    return redirect(url_for('api.user'))