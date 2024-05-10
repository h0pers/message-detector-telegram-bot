from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config import MessageText
from bot.database.main import SessionLocal
from bot.database.methods.create import create
from bot.database.models.channels import TriggerWordsList
from bot.fsm.admin import AdminStates

trigger_words_router = Router()


async def add_trigger_word(message: str):
    async with SessionLocal.begin() as session:
        await create(session, TriggerWordsList, values={'word': message})


@trigger_words_router.message(StateFilter(AdminStates.add_trigger_word), F.text)
async def add_trigger_words_handler(message: Message, state: FSMContext):
    messages = message.text.split(' ')

    for text in messages:
        await add_trigger_word(text)

    await message.answer(text=MessageText.ADD_TRIGGER_WORD_SUCCESSFUL)
    await state.set_state(AdminStates.edit_trigger_words)
