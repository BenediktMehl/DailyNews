from calendar import c
import logging
import asyncio
from fetchContent.llm_icon_chooser import choose_icons
from send.send_telegram_message import send_post_to_telegram
from fetchContent.rss_news_fetcher import fetch_top_news
from fetchContent.html_content_fetcher import fetch_html_contents
from buildPost.company_llm_summarizer import create_news_summaries
from buildPost.create_news_post import create_news_post
from buildPost.create_image import create_image
from datetime import datetime
import os

class NewsPostOrchestrator:
    def create_post_from_top_news(self, dir):
        logging.basicConfig(level=logging.INFO)
        
        top_news = fetch_top_news()
        contents = fetch_html_contents(top_news, 5)
        summaries = create_news_summaries(contents)
        choose_icons(summaries)
        
        os.makedirs(dir, exist_ok=True)

        create_news_post(summaries, top_news, dir)
        create_image(summaries, dir)

    def send_and_create_post(self):
        today_date_formatted = datetime.now().strftime("%Y-%m-%d")
        dir = f"posts/{today_date_formatted}"

        self.create_post_from_top_news(dir)
        asyncio.run(send_post_to_telegram(dir))
        
if __name__ == "__main__":
    orchestrator = NewsPostOrchestrator()
    orchestrator.send_and_create_post()

