import logging
import asyncio
from telegram import Bot # type: ignore
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
user_id = os.getenv('USER_ID')


async def main():
    bot = Bot(bot_token)
    await bot.send_message(chat_id=user_id, text="Hello World!")

if __name__ == '__main__':
    asyncio.run(main())
