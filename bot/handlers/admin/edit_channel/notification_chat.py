from aiogram import Router, F
from aiogram.filters import StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import update

from bot.config import MessageText
from bot.database.main import SessionLocal
from bot.database.models.channels import ObservingChannels
from bot.filters.state_data_has import StateDataHas
from bot.fsm.admin import AdminStates

notification_chat_router = Router()


@notification_chat_router.message(StateFilter(AdminStates.edit_notification_chat),
                                  or_f(F.text.is_numeric(), F.text.startswith('-')),
                                  StateDataHas(['chat_username']))
async def set_notification_chat_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    chat_id = int(message.text)
    chat_username = data['chat_username'].split('@', maxsplit=1)[-1]
    async with SessionLocal.begin() as session:
        query = update(ObservingChannels) \
            .where(ObservingChannels.invite_link == f'https://t.me/{chat_username}') \
            .values(notification_chat_id=chat_id)
        await session.execute(query)

    await message.answer(text=MessageText.NOTIFICATION_CHAT_SUCCESSFUL)
    await state.set_state(AdminStates.edit_chosen_channel)
