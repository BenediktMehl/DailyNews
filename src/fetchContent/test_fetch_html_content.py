import unittest
from src.fetchContent.fetch_html_content import fetch_html_contents


class TestFetchHTMLContent(unittest.TestCase):
    def test_fetch_html_contents(self):
        topics = [
            {'title': 'Wikipedia', 'url': 'https://www.wikipedia.org/'},
            {'title': 'Python', 'url': 'https://www.python.org/'},
        ]
        max_number_of_contents = 2

        contents = fetch_html_contents(topics, max_number_of_contents)

        self.assertEqual(len(contents), 2)
        self.assertEqual(contents[0]['title'], 'Wikipedia')
        self.assertEqual(contents[0]['url'], 'https://www.wikipedia.org/')
        self.assertTrue(isinstance(contents[0]['content'], str))
        self.assertGreater(len(contents[0]['content']), 0)

        self.assertEqual(contents[1]['title'], 'Python')
        self.assertEqual(contents[1]['url'], 'https://www.python.org/')
        self.assertTrue(isinstance(contents[1]['content'], str))
        self.assertGreater(len(contents[1]['content']), 0)

    def test_fetch_html_contents_short_raw_text(self):
        topics = [
            {'title': 'No Content', 'url': 'https://httpbin.org/status/404'},
        ]

        contents = fetch_html_contents(topics)

        self.assertEqual(len(contents), 0)


if __name__ == '__main__':
    unittest.main()
