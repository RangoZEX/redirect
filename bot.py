import os
import asyncio
import time
import logging
from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

try:
    API_ID = int(os.environ.get("API_ID", 15316304))
    API_HASH = os.environ.get("API_HASH", "bd4e50df87a06ac57d4926fab706c583")
    BOT_TOKENS = [token for token in os.environ.get("BOT_TOKEN", "").split()]
    if not API_ID or not API_HASH or not BOT_TOKENS:
        raise ValueError("API_ID, API_HASH, or BOT_TOKEN is missing or invalid.")
except Exception as e:
    logger.error(f"Environment variable error: {e}")
    exit(1)


async def send_reply(c, m):
    try:
        last_name = f' {getattr(m.from_user, "last_name", "")}'  # Use getattr to safely access last_name
        mention = f"[{m.from_user.first_name}{last_name}](tg://user?id={m.from_user.id})"
        user_full_name = f"{m.from_user.first_name} {getattr(m.from_user, 'last_name', '')}" if m.from_user.first_name else m.from_user.first_name or str(m.from_user.id)
        
        logger.info(f"Sending message to 👨 - {user_full_name}")
        
        inline_button = InlineKeyboardButton("Join @UploadXPro_Bot", url="https://t.me/UploadXPro_Bot")
        inline_keyboard = InlineKeyboardMarkup([[inline_button]])

        await m.reply_text(
            f"**👋 Hello {mention}**,\n\n"
            "<blockquote>**__🚀 This bot has now permanently shifted to **[UploadXPro](https://t.me/UploadXPro_Bot)** for better features and an enhanced experience.__**</blockquote>\n\n"
            "✨ **Why move?**\n"
            "- Faster uploads 🚄\n"
            "- More reliability 🔒\n"
            "- Additional tools and features 🎉\n\n"
            "👉 **Join now and try it out:** [UploadXPro](https://t.me/UploadXPro_Bot)\n\n"
            "Thank you for your support! 💙",
            reply_markup=inline_keyboard,
            quote=True,
            disable_web_page_preview=True
        )
        await asyncio.sleep(1)

    except FloodWait as e:
        logger.warning(f"Flood wait for {e.x} seconds. Retrying...")
        await asyncio.sleep(e.x)
        await send_reply(c, m)
    except Exception as e:
        logger.error(f"Failed to send shift message: {e}")
        

def initialize_bot(token, index):
    try:
        bot = Client(f"bot_{index}", bot_token=token, api_id=API_ID, api_hash=API_HASH)
        bot.add_handler(MessageHandler(send_reply))
        return bot
    except Exception as e:
        logger.error(f"Failed to initialize bot {index}: {e}")
        return None

def main():
    try:
        logger.info("Initializing bots...")
        bots = [initialize_bot(token, index) for index, token in enumerate(BOT_TOKENS, start=1)]

        for index, bot in enumerate(bots, start=1):
            if bot:
                logger.info(f"Starting Bot {index}...")
                bot.start()
                logger.info(f"Bot {index} started successfully.")

        logger.info("All bots are running.")
        asyncio.get_event_loop().run_forever()

    except KeyboardInterrupt:
        logger.info("Shutdown signal received. Stopping bots...")

if __name__ == "__main__":
    main()
