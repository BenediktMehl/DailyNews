import unittest
from rss_news_fetcher import RSSNewsFetcher

class TestRSSNewsFetcher(unittest.TestCase):
    def setUp(self):
        self.api_url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
        self.news_fetcher = RSSNewsFetcher(self.api_url)

    def test_fetch_news(self):
        news_items = self.news_fetcher.fetch_news()
        self.assertTrue(len(news_items) > 0, "No news items retrieved from RSS feed")

if __name__ == '__main__':
    unittest.main()
