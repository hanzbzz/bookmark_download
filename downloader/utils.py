import tweepy
from typing import List
from . import models


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
            result[tweet.id] = models.TweetInfo(tweet.id, "text",tweet.text, [""]).to_dict()
        else:
            keys = tweet.attachments['media_keys']
            urls = get_media_urls(keys, media_dict)
            media_type = media_dict[keys[0]].type
            result[tweet.id] = models.TweetInfo(tweet.id,media_type, tweet.text, urls).to_dict()
    
    return result