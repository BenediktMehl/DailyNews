import logging
import re
import requests

def fetch_top_news(number_of_news=None):
    return fetch_top_news_from(number_of_news, "http://hn.algolia.com/api/v1/search?tags=front_page")

def fetch_top_news_from(number_of_news, api_url):
    logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Fetch: Fetching top news from API URL: {api_url}")
    response = requests.get(api_url)
    news_items = response.json()['hits']
    logging.info(f"Fetch: Fetched {len(news_items)} news items")
    if( number_of_news is None):
        return news_items
    return news_items[:number_of_news]
