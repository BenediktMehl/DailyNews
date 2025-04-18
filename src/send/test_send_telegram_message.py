import unittest
import asyncio
from src.send.send_telegram_message import send_post_to_telegram

class TestSendTelegramMessage(unittest.TestCase):
    def test_send_post_to_telegram(self):
        output_dir = f"posts/test-10-10-2010"
        asyncio.run(send_post_to_telegram(output_dir))

if __name__ == '__main__':
    unittest.main()