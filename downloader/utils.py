import shutil
import tweepy
from typing import List, Union
from . import models
import random
import string
import os
import requests


def media_list_to_dict(media: List[tweepy.Media]):
    return {m.media_key: m for m in media}


def get_best_bitrate_url(media: tweepy.Media):
    best_rate = 0
    url = ""
    for variant in media.variants:
        if variant.get('bit_rate') is not None and variant['bit_rate'] > best_rate:
            best_rate = variant['bit_rate']
            url = variant['url']
    return url


def get_media_urls(keys, media_dict):
    urls = []
    for key in keys:
        media = media_dict[key]
        if media.type == "video":
            url = get_best_bitrate_url(media)
            urls.append(url)
        
        if media.type == "photo":
            urls.append(media.url)

    return urls


def parse_bookmarks(tweets: List[tweepy.Tweet], media: List[tweepy.Media]):
    result = {}
    media_dict = media_list_to_dict(media)
    
    for tweet in tweets:
        if tweet.attachments is None:
            result[tweet.id] = models.TweetInfo("text",tweet.text, []).to_dict()
        else:
            keys = tweet.attachments['media_keys']
            urls = get_media_urls(keys, media_dict)
            media_type = media_dict[keys[0]].type
            result[tweet.id] = models.TweetInfo(media_type, tweet.text, urls).to_dict()
    
    return result

def make_random_dir(name_length: int):
    dir_name = "".join(random.choice(string.ascii_letters + string.digits)for _ in range(name_length))
    os.mkdir("downloads/" + dir_name)
    return "downloads/" + dir_name

def download_tweets(tweets: dict[str, dict], selected_types: List[str], include_text: bool):
    dir_path = make_random_dir(12)
    for id in tweets.keys():
        tweet = tweets[id]
        tweet_type = tweet["type"]

        if tweet_type in selected_types:
            if tweet_type == "text":
                download_text_tweet(id, tweet, dir_path)
            elif tweet_type == "photo":
                download_media_tweet(id ,tweet, dir_path, include_text, "jpg")
            else :
                download_media_tweet(id ,tweet, dir_path, include_text, "mp4")
    return dir_path
        
def download_text_tweet(id:str, tweet: dict[str, Union[str, List[str]]], dir_path: str):
    with open(f"{dir_path}/{id}.txt", "w") as f:
        f.write(tweet["text"])


def download_media_tweet(id:str, tweet: dict[str, Union[str, List[str]]], dir_path: str, include_text: bool, extension: str):
    no = 1
 
    for url in tweet["media_urls"]:
        data = requests.get(url).content
        with open(f"{dir_path}/{id}{'_' + str(no) if len(tweet['media_urls']) > 1 else ''}.{extension}","wb") as handler:
            handler.write(data)
        no += 1
    if include_text:
        download_text_tweet(id, tweet, dir_path)


def cleanup(path: str):
    try:
        shutil.rmtree(path)
        os.remove(path + ".zip")
        return True
    except Exception:
        return False

