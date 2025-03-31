from buildPost.generate_post import create_news_post
import unittest
import os
from datetime import datetime


class TestCreateNewsPost(unittest.TestCase):
    def test_create_news_post(self):
        news_topics = [
            {"icon": "🌍", "entry_sentence": "Breaking news on climate change.", "detail": "The latest updates on global warming."},
            {"icon": "🌍", "entry_sentence": "AI advancements are here.", "detail": "New breakthroughs in artificial intelligence."},
            {"icon": "🌍", "entry_sentence": "Quantum computing evolves.", "detail": "The future of quantum technology is bright."},
            {"icon": "🌍", "entry_sentence": "Space exploration continues.", "detail": "NASA announces new missions to Mars."}
        ]

        top_news = [
            {"url": "https://example.com/news1"},
            {"url": "https://example.com/news2"},
            {"url": "https://example.com/news3"},
            {"url": "https://example.com/news4"}
        ]

        output_dir = f"posts/test-10-10-2010"
        output_file_path = f"{output_dir}/post.txt"

        os.makedirs(output_dir, exist_ok=True)

        create_news_post(news_topics, top_news, output_dir)

        self.assertTrue(os.path.exists(output_file_path), "The post file was not created.")

        with open(output_file_path, "r") as file:
            file_content = file.read()

        self.assertIn("🌍 *Breaking news on climate change.* The latest updates on global warming. https://example.com/news1", file_content)
        self.assertIn("🌍 *AI advancements are here.* New breakthroughs in artificial intelligence. https://example.com/news2", file_content)
        self.assertIn("🌍 *Quantum computing evolves.* The future of quantum technology is bright. https://example.com/news3", file_content)
        self.assertIn("🌍 *Space exploration continues.* NASA announces new missions to Mars. https://example.com/news4", file_content)


if __name__ == '__main__':
    unittest.main()
