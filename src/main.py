import logging
import asyncio
from send.send_telegram_message import send_telegram_message
import requests
from fetchContent.rss_news_fetcher import fetch_news
from buildPost.company_llm_summarizer import create_news_summary
from buildPost.create_news_post import create_news_post


class NewsPostOrchestrator:

    def create_post_from_top_news(self, api_url):
        logging.basicConfig(level=logging.INFO)
        logging.info("Fetching top 3 news items")
        top_news = fetch_news(api_url)[:3]
        logging.info("Importing requests module")
        summaries = []
        urls = []

        for news_id in top_news:
            news_item_url = f"https://hacker-news.firebaseio.com/v0/item/{news_id}.json?print=pretty"
            logging.info(f"Fetching news item details for ID: {news_id}")
            news_item = requests.get(news_item_url).json()
            logging.info(f"Fetched news item: {news_item}")
            logging.info(f"Creating summary for news item: {news_item.get('title', '')}")
            summary = create_news_summary(news_item.get('title', ''))
            logging.info(f"Created summary: {summary}")
            if summary != 'null':
                summaries.append(summary)
                urls.append(news_item.get('url', news_item_url))

        # Create the news post
        logging.info("Creating news post")
        news_post = create_news_post(summaries, urls)
        logging.info("News post created successfully")
        logging.info("Sending news post to Telegram")
        asyncio.run(send_telegram_message(news_post))
        logging.info("News post sent to Telegram successfully")


if __name__ == "__main__":
    orchestrator = NewsPostOrchestrator()
    api_url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    orchestrator.create_post_from_top_news(api_url)
