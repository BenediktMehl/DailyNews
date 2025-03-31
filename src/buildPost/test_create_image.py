from create_image import create_image
import unittest
import os
from datetime import datetime
from PIL import Image

class TestNewsImageCreation(unittest.TestCase):
    def test_image_creation(self):
        output_dir = f"posts/test-10-10-2010"
        output_path = f"{output_dir}/image.png"

        news_topics = [
            {
                "headline": "Latest updates on climate change and impact",
                "icon": "🌍",
            },
            {
                "headline": "New advancements in AI technology and applications",
                "icon": "🤖",
            },
            {
                "headline": "Breakthroughs in quantum computing and potential",
                "icon": "⚛️",
            }
        ]

        os.makedirs(output_dir, exist_ok=True)

        create_image(news_topics, output_dir)

        self.assertTrue(os.path.exists(output_path), "The image file was not created.")

        with Image.open(output_path) as img:
            # Check the image size
            self.assertEqual(img.size, (1024, 1064), "The image size is incorrect.")

            self.assertEqual(img.mode, "RGB", "The image mode is not RGB.")

if __name__ == '__main__':
    unittest.main()