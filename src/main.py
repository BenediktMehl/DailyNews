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
        logging.info("Fetch: Top 3 news items")
        top_news = fetch_top_news()
        summaries = []
        urls = []

        for news_id in top_news:
            news_item_url = f"https://hacker-news.firebaseio.com/v0/item/{news_id}.json?print=pretty"
            logging.info(f"Fetch: News item details for ID: {news_id}")
            news_item = requests.get(news_item_url).json()
            logging.info(f"Fetch: News item fetched: {{'by': {news_item['by']}, 'descendants': {news_item['descendants']}, 'id': {news_item['id']}, 'score': {news_item['score']}, 'time': {news_item['time']}, 'title': {news_item['title']}, 'type': {news_item['type']}, 'url': {news_item['url']}}}")
            logging.info(f"AI Interaction: Creating summary for news item: {news_item.get('title', '')}")
            summary = create_news_summary(news_item.get('title', ''))
            if summary is None:
                logging.warning(f"AI Interaction: Failed to create summary for news item: {news_item.get('title', '')}")
            else:
                logging.info(f"AI Interaction: Created summary: {summary}")
                summaries.append(summary)
                urls.append(news_item.get('url', news_item_url))

        logging.info("AI Interaction: Creating news post")
        news_post = create_news_post(summaries, urls)
        logging.info("AI Interaction: News post created successfully")
        logging.info(f"Resulting Post: {news_post}")
        logging.info("Fetch: Sending news post to Telegram")
        asyncio.run(send_telegram_message(news_post))


if __name__ == "__main__":
    orchestrator = NewsPostOrchestrator()
    api_url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    orchestrator.create_post_from_top_news(api_url)
