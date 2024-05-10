from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config import MessageText
from bot.database.main import SessionLocal
from bot.database.methods.get import get
from bot.database.models.channels import Settings
from bot.fsm.admin import AdminStates

notification_chat_router = Router()


@notification_chat_router.message(StateFilter(AdminStates.edit_notification_chat),
                                  F.text)
async def set_notification_chat_handler(message: Message, state: FSMContext):
    notification_chat_id = int(message.text)
    async with SessionLocal.begin() as session:
        settings = (await get(session, Settings, id=1)).scalar()
        settings.notification_chat_id = notification_chat_id

    await message.answer(text=MessageText.NOTIFICATION_CHAT_SUCCESSFUL)
    await state.set_state(AdminStates.edit_chosen_channel)
