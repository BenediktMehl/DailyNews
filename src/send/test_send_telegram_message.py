import unittest
import asyncio
from src.send.send_telegram_message import send_telegram_message

class TestSendTelegramMessage(unittest.TestCase):
    def test_send_message(self):
        message = "Test message"
        asyncio.run(send_telegram_message(message))
        # Since this is an integration test, you would verify the message was sent by checking the Telegram chat manually

if __name__ == '__main__':
    unittest.main()
