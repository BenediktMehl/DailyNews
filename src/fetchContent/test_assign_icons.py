import unittest
from fetchContent.assign_icons import choose_icons

class TestCreateNewsSummary(unittest.TestCase):
    def test_create_news_summary(self):
        news_topics = [
            {"entry_sentence": "Breaking news on climate change.", "detail": "The latest updates on global warming."}
        ]

        choose_icons(news_topics)
        
        icon = news_topics[0]["icon"]
        self.assertEqual(icon, "🌍")

if __name__ == '__main__':
    unittest.main()