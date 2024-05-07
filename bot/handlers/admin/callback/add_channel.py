from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callback.admin.panel import AdminPanelCallback
from bot.config import MessageText
from bot.fsm.admin import AdminStates

add_chanel_router = Router()


@add_chanel_router.callback_query(StateFilter(None), AdminPanelCallback.filter(F.ADD_OBSERVING_CHANNEL == 1))
async def add_channel_handler(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=MessageText.ADD_CHANNEL)
    await state.set_state(AdminStates.add_channel)
    await query.answer()
