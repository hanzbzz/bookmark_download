from typing import List

class TweetInfo:
    def __init__(self, type: str, text: str, media_urls: List[str]) -> None:
        self.type = type
        self.text = text
        self.media_urls = media_urls

    def to_dict(self):
        return {
        "type": self.type,
        "text": self.text,
        "media_urls": self.media_urls
        }