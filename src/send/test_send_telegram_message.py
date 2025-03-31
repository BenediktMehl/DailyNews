import unittest
import asyncio
from send_telegram_message import send_telegram_message
from PIL import Image

class TestSendTelegramMessage(unittest.TestCase):
    def test_send_message(self):
        # Define the test image and message
        image = Image.new('RGB', (1024, 1024), color=(128, 0, 128))
        message_text = "This is a test message with an image."

        # Create the news_post tuple
        news_post = (image, message_text)

        # Run the send_telegram_message function
        asyncio.run(send_telegram_message(news_post))

        # Since this is an integration test, verify the message and image were sent by checking the Telegram chat manually

if __name__ == '__main__':
    unittest.main()