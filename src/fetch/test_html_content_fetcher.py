import unittest
from src.fetch.html_content_fetcher import HTMLContentFetcher


class TestHTMLContentFetcher(unittest.TestCase):
    def test_get_html_content(self):
        url = "https://victorpoughon.fr/i-tried-making-artificial-sunlight-at-home/"
        fetcher = HTMLContentFetcher()
        content = fetcher.get_html_content(url)
        self.assertTrue(isinstance(content, str))
        self.assertGreater(len(content), 0)

    def test_print_html_content(self):
        url = "https://victorpoughon.fr/i-tried-making-artificial-sunlight-at-home/"
        fetcher = HTMLContentFetcher()
        content = fetcher.get_html_content(url)
        print(content)


if __name__ == '__main__':
    unittest.main()
