from typing import List

class TweetInfo:
    def __init__(self, id: str, type: str, text: str, media_urls: List[str]) -> None:
        self.id = id
        self.type = type
        self.text = text
        self.media_urls = media_urls

    def to_dict(self):
        return {
        "id": self.id,
        "type": self.type,
        "text": self.text,
        "media_urls": self.media_urls
        }