import os
import asyncio
import logging
from pyrogram import Client
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

# Initialize a bot
def initialize_bot(token, index):
    try:
        bot = Client(f"bot_{index}", bot_token=token, api_id=API_ID, api_hash=API_HASH)
        bot.add_handler(MessageHandler(send_reply))
        return bot
    except Exception as e:
        logger.error(f"Failed to initialize bot {index}: {e}")
        return None

# Main function
def main():
    try:
        logger.info("Initializing bots...")
        bots = [initialize_bot(token, index) for index, token in enumerate(BOT_TOKENS, start=1)]

        for index, bot in enumerate(bots, start=1):
            if bot:
                logger.info(f"Starting Bot {index}...")
                bot.start()
                logger.info(f"Bot {index} started successfully.")

        logger.info("All bots are running. Press Ctrl+C to stop.")
        asyncio.get_event_loop().run_forever()

    except KeyboardInterrupt:
        logger.info("Shutdown signal received. Stopping bots...")
    finally:
        for index, bot in enumerate(bots, start=1):
            if bot:
                bot.stop()
                logger.info(f"Bot {index} stopped.")
        logger.info("All bots stopped gracefully.")

if __name__ == "__main__":
    main()
