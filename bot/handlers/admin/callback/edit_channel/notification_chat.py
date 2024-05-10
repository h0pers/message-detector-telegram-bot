from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callback.admin.panel import AdminPanelCallback
from bot.config import MessageText
from bot.fsm.admin import AdminStates

notification_chat_callback_router = Router()


@notification_chat_callback_router.callback_query(StateFilter(None),
                                                  AdminPanelCallback.filter(F.EDIT_CHANNEL_NOTIFICATION_CHAT == 1))
async def edit_notification_chat_handler(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=MessageText.SET_NOTIFICATION_CHAT)
    await state.set_state(AdminStates.edit_notification_chat)
    await query.answer()
