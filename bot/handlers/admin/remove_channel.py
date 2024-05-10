from aiogram import Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config import MessageText
from bot.database.main import SessionLocal
from bot.database.methods.delete import delete
from bot.database.methods.get import get
from bot.database.models.channels import ObservingChannels
from bot.filters.document_type import DocumentType
from bot.fsm.admin import AdminStates

remove_channel_router = Router()


@remove_channel_router.message(StateFilter(AdminStates.remove_channel),
                               DocumentType(['.txt']))
async def remove_channel_handler(message: Message, bot: Bot, state: FSMContext):
    file_binary = await bot.download(message.document)

    with file_binary as file:
        content = file.read().decode()
        links = content.split('\n')

    async with SessionLocal.begin() as session:
        for link in links:
            try:
                await delete(session, ObservingChannels, invite_link=link)
            except:
                await message.answer(text=MessageText.REMOVE_CHANNEL_ERROR.format(link=link))

    await message.answer(text=MessageText.REMOVE_CHANNEL_SUCCESSFUL)
    await state.clear()
