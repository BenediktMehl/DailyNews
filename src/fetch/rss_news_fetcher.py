import requests
from news_fetcher import NewsFetcher

class RSSNewsFetcher(NewsFetcher):
    def __init__(self, api_url):
        super().__init__()
        self.api_url = api_url

    def fetch_news(self):
        response = requests.get(self.api_url)
        news_items = response.json()
        return news_items
