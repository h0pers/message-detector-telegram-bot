from typing import List

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config import MessageText
from bot.database.main import SessionLocal
from bot.database.methods.create import create
from bot.database.methods.get import get
from bot.database.models.channels import TriggerWordsList, ObservingChannels
from bot.filters.state_data_has import StateDataHas
from bot.fsm.admin import AdminStates

trigger_words_router = Router()


async def add_trigger_word(message: str, chat_username: str):
    chat_username = chat_username.split('@', maxsplit=1)[-1]
    async with SessionLocal.begin() as session:
        channel = (await get(session,
                             ObservingChannels,
                             invite_link=f'https://t.me/{chat_username}')).scalar()

        await create(session, TriggerWordsList, values={'word': message, 'channel_id': channel.id})


@trigger_words_router.message(StateFilter(AdminStates.add_trigger_word), F.text, StateDataHas(['chat_username']))
async def add_trigger_words_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    messages = message.text.split(' ')

    for text in messages:
        await add_trigger_word(text, data['chat_username'])

    await message.answer(text=MessageText.ADD_TRIGGER_WORD_SUCCESSFUL)
    await state.set_state(AdminStates.edit_trigger_words)
