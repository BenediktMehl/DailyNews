import unittest
from fetch_urls import fetch_top_news


class TestFetchTopNews(unittest.TestCase):
    def test_fetch_top_news(self):
        topics = [{'title': 'Existing Topic', 'url': 'https://example.com'}]
        news_items = fetch_top_news(topics)
        self.assertTrue(len(news_items) > len(topics))
        self.assertTrue(all('title' in item and 'url' in item for item in news_items))


if __name__ == '__main__':
    unittest.main()
