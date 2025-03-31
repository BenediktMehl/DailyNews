import logging
import requests

def fetch_top_news(topics):
    return topics + fetch_top_news_from("http://hn.algolia.com/api/v1/search?tags=front_page")

def fetch_top_news_from(api_url):
    logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Fetch: Fetching top news from API URL: {api_url}")
    response = requests.get(api_url)
    json_response = response.json()['hits']
    logging.info(f"Fetch: Fetched {len(json_response)} news items")
    return json_response
