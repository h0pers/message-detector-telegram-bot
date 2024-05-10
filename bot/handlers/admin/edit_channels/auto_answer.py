from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callback.admin.panel import AdminPanelCallback
from bot.config import MessageText
from bot.database.main import SessionLocal
from bot.database.methods.get import get
from bot.database.models.channels import ObservingChannels, Settings
from bot.filters.state_data_has import StateDataHas
from bot.fsm.admin import AdminStates
from bot.keyboards.inline.admin.edit_auto_answer import edit_auto_answer_inline_markup

auto_answer_router = Router()


@auto_answer_router.message(StateFilter(AdminStates.add_auto_answer), F.text)
async def set_auto_message(message: Message, state: FSMContext):

    async with SessionLocal.begin() as session:
        settings = (await get(session, Settings, id=1)).scalar()
        settings.auto_answer_text = message.text
        settings.is_auto_answer_enable = True

    await message.answer(text=MessageText.AUTO_ANSWER_SUCCESSFUL)
    await state.set_state(AdminStates.edit_auto_answer)
