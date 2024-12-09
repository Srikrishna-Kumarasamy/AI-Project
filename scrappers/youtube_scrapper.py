import uuid
import requests
from dataclasses import asdict
from store_in_mongo_db import MongoDB
from data_modules.content import Content
from youtube_transcript_api import YouTubeTranscriptApi


class YoutubeScrapper:

    def __init__(self):
        self.SOURCE = "Youtube"
        self.mongo_db = MongoDB()

    def get_video_id(self):
        return self.youtube_url.split("v=")[1].split("&")[0]
    
    def get_video_title(self):
        formatted_url = f"https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={self.video_id}&format=json"
        response = requests.get(formatted_url)
        if response.status_code == 200:
            return response.json()['title']
        return None

    def get_transcript(self):
        transcript = YouTubeTranscriptApi.get_transcript(self.video_id)
        return " ".join([entry['text'] for entry in transcript])

    def scrape(self, youtube_url):
        self.youtube_url = youtube_url
        self.video_id = self.get_video_id()
        self.content = Content(
            _id = str(uuid.uuid4()),
            title = self.get_video_title(),
            source = self.SOURCE,
            url = self.youtube_url,
            description = self.get_transcript()
        )
        # self.store_in_mongo_db(asdict(self.content))
        return asdict(self.content)
