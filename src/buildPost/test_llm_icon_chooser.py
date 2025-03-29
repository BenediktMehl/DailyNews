import unittest
from unittest.mock import patch, MagicMock
from llm_icon_chooser import choose_icon

class TestCreateNewsSummary(unittest.TestCase):
    def test_create_news_summary(self):
        icon = choose_icon("Latest updates on climate change")
        
        self.assertEqual(icon, "🌍")

if __name__ == '__main__':
    unittest.main()