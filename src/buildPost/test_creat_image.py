from create_image import create_image 
import unittest
import os

class TestNewsImageCreation(unittest.TestCase):
    def test_image_creation(self):
        output_path = 'src/buildPost/test_output_image.png'
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


        # Create the image
        img = create_image(news_topics)
        
        # Save the image to a file
        img.save(output_path)

        # Check if the image exists
        self.assertTrue(os.path.exists(output_path))
        
        # Check the image size
        self.assertEqual(img.size, (1024, 1024))

if __name__ == '__main__':
    unittest.main()
