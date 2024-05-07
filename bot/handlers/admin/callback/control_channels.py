from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callback.admin.panel import AdminPanelCallback
from bot.config import MessageText
from bot.filters.state_data_has import StateDataHas
from bot.fsm.admin import AdminStates
from bot.handlers.admin.callback.channels_list import get_channels_keyboard_markup
from bot.keyboards.inline.admin.edit_channel_features import edit_channel_inline_markup

control_chanel_router = Router()


@control_chanel_router.callback_query(StateFilter(None), AdminPanelCallback.filter(F.CONTROL_OBSERVING_CHANNELS == 1))
async def control_channel_handler(query: CallbackQuery, state: FSMContext):
    channels_keyboard = await get_channels_keyboard_markup()
    if not channels_keyboard.inline_keyboard:
        await query.answer(MessageText.NO_DATA)
        return

    await state.set_state(AdminStates.control_channels)
    await query.message.edit_text(text=MessageText.CONTROL_CHANNELS, reply_markup=channels_keyboard)
    await query.answer()


@control_chanel_router.callback_query(StateFilter(AdminStates.control_channels), F.data.startswith('@'))
async def select_channel_to_edit_handler(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(text=MessageText.CONTROL_CHANNEL.format(chat_username=query.data),
                                  reply_markup=edit_channel_inline_markup.get_markup())
    await state.set_state(AdminStates.edit_chosen_channel)
    await state.update_data({'chat_username': query.data})
    await query.answer()

