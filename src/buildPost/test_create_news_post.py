import unittest
from src.buildPost.create_news_post import create_news_post

class TestCreateNewsPost(unittest.TestCase):
    def test_create_news_post(self):
        summaries = [
            "Summary 1",
            "Summary 2",
            "Summary 3",
            "Summary 4"
        ]

        urls = [
            "https://example.com/news1",
            "https://example.com/news2",
            "https://example.com/news3",
            "https://example.com/news4"
        ]

        formatted_post = create_news_post(summaries, urls)

        # Verify the generated post
        self.assertIn("🌟 Summary 1 https://example.com/news1", formatted_post)
        self.assertIn("🌟 Summary 2 https://example.com/news2", formatted_post)
        self.assertIn("🌟 Summary 3 https://example.com/news3", formatted_post)
        self.assertIn("🌟 Summary 4 https://example.com/news4", formatted_post)

        print(formatted_post)

if __name__ == '__main__':
    unittest.main()
