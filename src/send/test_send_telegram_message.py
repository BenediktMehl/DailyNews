import unittest
import asyncio
from send_telegram_message import send_telegram_message

class TestSendTelegramMessage(unittest.TestCase):
    def test_send_message(self):
        # Define the test image and message
        image_path = "src/buildPost/test_output_image.png"
        message_text = "This is a test message with an image."

        # Create the news_post tuple
        news_post = (image_path, message_text)

        # Run the send_telegram_message function
        asyncio.run(send_telegram_message(news_post))

        # Since this is an integration test, verify the message and image were sent by checking the Telegram chat manually

if __name__ == '__main__':
    unittest.main()