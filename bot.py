import os
import asyncio
import logging
from pyrogram import Client, compose
from pyrogram.handlers import MessageHandler

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
try:
    API_ID = int(os.environ.get("API_ID", 15316304))
    API_HASH = os.environ.get("API_HASH", "bd4e50df87a06ac57d4926fab706c583")
    BOT_TOKENS = [token for token in os.environ.get("BOT_TOKEN", "").split()]
    if not API_ID or not API_HASH or not BOT_TOKENS:
        raise ValueError("API_ID, API_HASH, or BOT_TOKEN is missing or invalid.")
except Exception as e:
    logger.error(f"Environment variable error: {e}")
    exit(1)

# Message handler
async def send_reply(client, message):
    try:
        await message.reply_text(
            "**👋 Hello there!**\n\n"
            "__🚀 This bot has now permanently shifted to **[UploadXPro](https://t.me/UploadXPro_Bot)** for better features and an enhanced experience.__\n\n"
            "✨ **Why move?**\n"
            "- Faster uploads 🚄\n"
            "- More reliability 🔒\n"
            "- Additional tools and features 🎉\n\n"
            "👉 **Join now and try it out:** [UploadXPro](https://t.me/UploadXPro_Bot)\n\n"
            "_Thank you for your support! 💙_",
            quote=True,
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Failed to send shift message: {e}")

# Initialize and run multiple bots
async def initialize_bot(token, index):
    try:
        bot = Client(f"bot_{index}", bot_token=token, api_id=API_ID, api_hash=API_HASH)
        bot.add_handler(MessageHandler(send_reply))
        await bot.start()
        logger.info(f"Bot {index} started successfully.")
        return bot
    except Exception as e:
        logger.error(f"Failed to initialize bot {index}: {e}")
        return None

async def main():
    bots = []
    try:
        logger.info("Starting bots...")
        for index, token in enumerate(BOT_TOKENS, start=1):
            bot = await initialize_bot(token, index)
            if bot:
                bots.append(bot)

        if not bots:
            logger.error("No bots were successfully started. Exiting.")
            return

        logger.info("All bots are running.")
        await compose(bots)

    except KeyboardInterrupt:
        logger.info("Shutdown signal received. Stopping bots...")
    finally:
        for index, bot in enumerate(bots, start=1):
            await bot.stop()
            logger.info(f"Bot {index} stopped.")
        logger.info("All bots stopped gracefully.")

if __name__ == "__main__":
    asyncio.run(main())
