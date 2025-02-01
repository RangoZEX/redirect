import os
import asyncio
import logging
from aiohttp import web
from message import REDIRECT_MSG
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait, BadRequest

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    API_ID = int(os.environ.get("API_ID", 15316304))
    API_HASH = os.environ.get("API_HASH", "bd4e50df87a06ac57d4926fab706c583")
    BOT_TOKENS = [token for token in os.environ.get("BOT_TOKEN", "").split()]
    PORT = int(os.environ.get("PORT", 8080))
    if not API_ID or not API_HASH or not BOT_TOKENS:
        raise ValueError("API_ID, API_HASH, or BOT_TOKEN is missing or invalid.")
except Exception as e:
    logger.error(f"Environment variable error: {e}")
    exit(1)

@Client.on_message(filters.incoming & filters.private, group=-1)
async def send_reply(c, m):
    if m.from_user:
        usr = m.from_user.first_name if m.from_user.first_name else 'User'
        user_id = m.from_user.id
        last_name = f' {m.from_user.last_name}' if m.from_user.last_name else ''
        mention = f"[{usr}{last_name}](tg://user?id={user_id})"

        try:
            inline_button = InlineKeyboardButton("🔰 Join @UploadXPro_Bot", url="https://t.me/UploadXPro_Bot")
            inline_keyboard = InlineKeyboardMarkup([[inline_button]])
            await m.reply_photo(
                photo="https://i.ibb.co/7jzPRn3/301-status-code.jpg",
                caption=REDIRECT_MSG,
                reply_markup=inline_keyboard,
                quote=True
            )
            logger.info(f"Moved prompt message sent to: 🙎 {usr}")
            await c.send_reaction(chat_id=m.chat.id, message_id=m.id, emoji="🥴", big=True)
        except FloodWait as e:
            logger.warning(f"Flood wait for {e.value} seconds. Retrying...")
            await asyncio.sleep(e.value)
        except Exception as e:
            logger.error(f"Got error while sending msg: {e}")
    else:
        logger.info("One idiot added bot on CHANNEL so I can't get user information")

def initialize_bot(token, index):
    try:
        bot = Client(f"bot_{index}", bot_token=token, api_id=API_ID, api_hash=API_HASH)
        bot.start()
        bot_info = bot.get_me()
        bot_username = bot_info.username

        logger.info(f"Bot {index} initialized successfully. Username: @{bot_username}")
        bot.add_handler(MessageHandler(send_reply))
        return bot
    except FloodWait as e:
        logger.warning(f"Flood wait for {e.value} seconds while initializing bot {index}. Skipping this bot.")
        return None
    except BadRequest as e:
        logger.error(f"Bot {index} failed to initialize. Invalid or expired token: {token[:10]}... | Error: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to initialize bot {index} with token {token[:10]}... | Error: {e}")
        return None

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response({"message": "Bot is running!"})

async def web_server():
    web_app = web.Application(client_max_size=30_000_000)
    web_app.add_routes(routes)
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info(f"Web server running on port {PORT}")

async def main():
    try:
        logger.info(f"Total bot tokens provided: {len(BOT_TOKENS)}")
        bots = []

        for index, token in enumerate(BOT_TOKENS, start=1):
            logger.info(f"Processing bot {index} with token: {token[:10]}...")
            bot = initialize_bot(token, index)
            if bot:
                bots.append(bot)

        if not bots:
            logger.error("❌ No bots were initialized. Exiting...")
            exit(1)

        logger.info(f"{len(bots)} bots initialized successfully. All bots are running.")
        await web_server()
        await asyncio.Future()

    except KeyboardInterrupt:
        logger.info("Shutdown signal received. Stopping bots...")
        for bot in bots:
            bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
