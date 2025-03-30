import logging
from telegram import Bot  # type: ignore
from dotenv import load_dotenv  # type: ignore
import os

load_dotenv()

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
user_id = os.getenv('USER_ID')


async def send_telegram_message(news_post):
    image, text = news_post
    logging.basicConfig(level=logging.INFO)
    logging.info("Fetch: Initializing Telegram Bot")
    bot = Bot(bot_token)

    # Send the image
    logging.info("AI Interaction: Sending image to Telegram")
    with open(image, 'rb') as img_file:  # Open the image file in binary mode
        await bot.send_photo(chat_id=user_id, photo=img_file)
    logging.info("AI Interaction: Image sent to Telegram successfully")

    # Send the text
    logging.info("AI Interaction: Sending message to Telegram")
    await bot.send_message(chat_id=user_id, text=text)
    logging.info("AI Interaction: Message sent to Telegram successfully")