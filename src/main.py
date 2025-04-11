from calendar import c
import logging
import asyncio
from fetchContent.assign_icons import choose_icons
from send.send_telegram_message import send_post_to_telegram
from fetchContent.fetch_urls import fetch_top_news
from fetchContent.fetch_html_content import fetch_html_contents
from fetchContent.ai_generate_topics import create_news_topics
from buildPost.generate_post import create_news_post
from buildPost.generate_image import create_image
from datetime import datetime
import os
import json


class NewsPostOrchestrator:
    def create_topics(self, dir):
        logging.basicConfig(level=logging.INFO)
        os.makedirs(dir, exist_ok=True)

        topics = []
        topics = fetch_top_news(topics)
        topics = fetch_html_contents(topics, 5)
        topics = create_news_topics(topics, 3)
        topics = choose_icons(topics)

        topics_file_path = f"{dir}/topics.json"
        with open(topics_file_path, "w") as json_file:
            json.dump(topics, json_file, indent=4)

    def create_post_and_image(self, dir):
        topics_file_path = f"{dir}/topics.json"
        with open(topics_file_path, "r") as json_file:
            topics = json.load(json_file)

        create_news_post(topics, dir)
        create_image(topics, dir)

    def send_and_create_post(self):
        today_date_formatted = datetime.now().strftime("%Y-%m-%d")
        dir = f"posts/{today_date_formatted}"

        self.create_topics(dir)
        self.create_post_and_image(dir)
        asyncio.run(send_post_to_telegram(dir))


if __name__ == "__main__":
    orchestrator = NewsPostOrchestrator()
    orchestrator.send_and_create_post()
