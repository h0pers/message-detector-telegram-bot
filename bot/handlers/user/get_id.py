from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.middleware.db_updates import CollectData

get_id_router = Router()

get_id_router.message.middleware(CollectData())


@get_id_router.message(Command(commands=['id']))
async def get_id_handler(message: Message):
    await message.answer(text=f'ID Чата: <code>{message.chat.id}</code>')
