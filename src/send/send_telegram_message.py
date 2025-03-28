import logging
import asyncio
from telegram import Bot # type: ignore
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
user_id = os.getenv('USER_ID')


async def send_telegram_message(text: str):
    logging.basicConfig(level=logging.INFO)
    logging.info("Fetch: Initializing Telegram Bot")
    bot = Bot(bot_token)
    logging.info("AI Interaction: Sending message to Telegram")
    await bot.send_message(chat_id=user_id, text=text)
    logging.info("AI Interaction: Message sent to Telegram successfully")
