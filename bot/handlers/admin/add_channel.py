from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config import MessageText
from bot.database.main import SessionLocal
from bot.database.methods.create import create
from bot.database.models.channels import ObservingChannels
from bot.filters.document_type import DocumentType
from bot.fsm.admin import AdminStates

add_chanel_router = Router()


@add_chanel_router.message(StateFilter(AdminStates.add_channel),
                           DocumentType(['.txt']))
async def add_channel_handler(message: Message, bot: Bot, state: FSMContext):
    file_binary = await bot.download(message.document)

    with file_binary as file:
        content = file.read().decode()
        links = content.split('\n')

    async with SessionLocal.begin() as session:
        for link in links:
            try:
                await create(session, ObservingChannels, values={'invite_link': link})

            except Exception as ex:
                await message.answer(text=MessageText.ADD_CHANNEL_ERROR.format(link=link))

    await message.answer(text=MessageText.ADD_CHANNEL_SUCCESSFUL)
    await state.clear()
