import logging
import requests

def fetch_news(api_url):
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Fetch: Fetching news from API URL: {api_url}")
    response = requests.get(api_url)
    news_items = response.json()
    logging.info(f"Fetch: Fetched {len(news_items)} news items")
    return news_items
