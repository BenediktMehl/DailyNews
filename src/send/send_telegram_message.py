import logging
from telegram import Bot
from dotenv import load_dotenv 
import os

load_dotenv()

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
user_id = os.getenv('USER_ID')


async def send_post_to_telegram(input_dir):
    file_text_path = f"{input_dir}/post.txt"
    with open(file_text_path, 'r') as file:
        text = file.read()

    file_image_path = f"{input_dir}/image.png"
    with open(file_image_path, 'rb') as image:
        image_data = image.read()

    await send_telegram_message(image_data, text)


async def send_telegram_message(image, text):
    logging.basicConfig(level=logging.INFO)
    logging.info("Fetch: Initializing Telegram Bot")
    bot = Bot(bot_token)

    # Send the image
    logging.info("AI Interaction: Sending image to Telegram")
    await bot.send_photo(chat_id=user_id, photo=image)
    logging.info("AI Interaction: Image sent to Telegram successfully")

    # Send the text
    logging.info("AI Interaction: Sending message to Telegram")
    await bot.send_message(chat_id=user_id, text=text)
    logging.info("AI Interaction: Message sent to Telegram successfully")