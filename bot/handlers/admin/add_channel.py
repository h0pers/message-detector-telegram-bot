from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config import MessageText
from bot.database.main import SessionLocal
from bot.database.methods.create import create
from bot.database.models.channels import ObservingChannels
from bot.fsm.admin import AdminStates

add_chanel_router = Router()


@add_chanel_router.message(StateFilter(AdminStates.add_channel), F.text.contains('https://t.me/'))
async def add_channel_handler(message: Message, state: FSMContext):
    async with SessionLocal.begin() as session:
        await create(session, ObservingChannels, values={'invite_link': message.text})

    await message.answer(text=MessageText.ADD_CHANNEL_SUCCESSFUL)
    await state.clear()
