import logging
import requests

def fetch_top_news(number_of_news, api_url="https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"):
    return fetch_top_news_from(number_of_news, api_url, "https://hacker-news.firebaseio.com/v0/item/{news_id}.json?print=pretty")

def fetch_top_news_from(number_of_news, api_url, news_item_url_template):
    logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Fetch: Fetching top news from API URL: {api_url}")
    response = requests.get(api_url)
    news_items = response.json()
    logging.info(f"Fetch: Fetched {len(news_items)} news items")
    top_news_ids = news_items[:number_of_news]
    top_news = []

    for news_id in top_news_ids:
        news_item_url = news_item_url_template.format(news_id=news_id)
        logging.info(f"Fetch: News item details for ID: {news_id}")
        news_item = requests.get(news_item_url).json()
        logging.info(f"Fetch: News item fetched: {{'by': {news_item['by']}, 'descendants': {news_item['descendants']}, 'id': {news_item['id']}, 'score': {news_item['score']}, 'time': {news_item['time']}, 'title': {news_item['title']}, 'type': {news_item['type']}, 'url': {news_item['url']}}}")
        top_news.append((news_item_url, news_item))

    return top_news
