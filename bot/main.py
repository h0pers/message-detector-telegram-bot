from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from pyrogram.handlers import MessageHandler
from redis.asyncio import Redis

from bot.database.models.main import register_models
from bot.filters.trigger_message import is_trigger_message
from bot.handlers.main import get_all_routers

from bot.config import BOT_TOKEN, REDIS_PORT, REDIS_HOST, TG_MONITORING_CLIENT, TG_CLIENT
from bot.handlers.other import trigger_message_handler

dp = Dispatcher(storage=RedisStorage(Redis(host=REDIS_HOST, port=REDIS_PORT)))


async def start_bot():
    await register_models()
    dp.include_routers(*get_all_routers())
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    await TG_MONITORING_CLIENT.connect()
    await dp.start_polling(bot)


def start_telegram_client():
    TG_CLIENT.add_handler(MessageHandler(trigger_message_handler, is_trigger_message))
    TG_CLIENT.run()

