from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callback.admin.panel import AdminPanelCallback
from bot.config import MessageText
from bot.database.main import SessionLocal
from bot.database.methods.get import get
from bot.database.models.channels import ObservingChannels
from bot.filters.state_data_has import StateDataHas
from bot.fsm.admin import AdminStates
from bot.keyboards.inline.admin.edit_auto_answer import edit_auto_answer_inline_markup

auto_answer_router = Router()


@auto_answer_router.message(StateFilter(AdminStates.add_auto_answer), F.text, StateDataHas(['chat_username']))
async def set_auto_message(message: Message, state: FSMContext):
    data = await state.get_data()
    chat_username = data['chat_username'].split('@', maxsplit=1)[-1]

    async with SessionLocal.begin() as session:
        channel = (await get(session, ObservingChannels, invite_link=f'https://t.me/{chat_username}')).scalar()
        channel.auto_answer_text = message.text
        channel.is_auto_answer_enable = True

    await message.answer(text=MessageText.AUTO_ANSWER_SUCCESSFUL)
    await state.set_state(AdminStates.edit_auto_answer)
