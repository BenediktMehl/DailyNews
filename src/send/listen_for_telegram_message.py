import asyncio
import telegram # type: ignore
from dotenv import load_dotenv # type: ignore
import os

# Load environment variables from .env file
load_dotenv()

# Get the bot token from environment variables
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

async def main():
    bot = telegram.Bot(bot_token)
    async with bot:
        updates = await bot.get_updates()
        if updates:
            user_id = updates[0].message.from_user.id
            print(f"User ID: {user_id}")

if __name__ == '__main__':
    asyncio.run(main())
