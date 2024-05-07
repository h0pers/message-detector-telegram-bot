from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callback.admin.panel import AdminPanelCallback
from bot.config import MessageText
from bot.database.main import SessionLocal
from bot.database.methods.get import get
from bot.database.models.channels import ObservingChannels
from bot.filters.state_data_has import StateDataHas
from bot.fsm.admin import AdminStates
from bot.keyboards.inline.admin.edit_auto_answer import edit_auto_answer_inline_markup

auto_answer_callback_router = Router()


@auto_answer_callback_router.callback_query(StateFilter(AdminStates.edit_chosen_channel),
                                            AdminPanelCallback.filter(F.EDIT_CHANNEL_AUTO_ANSWER == 1))
async def edit_auto_answer_handler(query: CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=edit_auto_answer_inline_markup.get_markup())
    await state.set_state(AdminStates.edit_auto_answer)
    await query.answer()


@auto_answer_callback_router.callback_query(StateFilter(AdminStates.edit_auto_answer),
                                            AdminPanelCallback.filter(F.ADD_AUTO_ANSWER == 1))
async def set_auto_answer_handler(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=MessageText.SET_AUTO_ANSWER)
    await state.set_state(AdminStates.add_auto_answer)
    await query.answer()


@auto_answer_callback_router.callback_query(StateFilter(AdminStates.edit_auto_answer),
                                            AdminPanelCallback.filter(F.SWITCH_AUTO_ANSWER == 1),
                                            StateDataHas(['chat_username']))
async def switch_auto_answer_handler(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chat_username = data['chat_username'].split('@', maxsplit=1)[-1]

    async with SessionLocal.begin() as session:
        channel = (await get(session, ObservingChannels, invite_link=f'https://t.me/{chat_username}')).scalar()
        await state.set_state(AdminStates.edit_auto_answer)
        if channel.auto_answer_text is None:
            await query.answer('NOT SET')
            return

        channel.is_auto_answer_enable = not channel.is_auto_answer_enable

    if not channel.is_auto_answer_enable:
        await query.answer('❌')

    await query.answer('✅')


@auto_answer_callback_router.callback_query(StateFilter(AdminStates.edit_auto_answer),
                                            AdminPanelCallback.filter(F.CLEAR_AUTO_ANSWER == 1),
                                            StateDataHas(['chat_username']))
async def clear_auto_answer_handler(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chat_username = data['chat_username'].split('@', maxsplit=1)[-1]

    async with SessionLocal.begin() as session:
        channel = (await get(session, ObservingChannels, invite_link=f'https://t.me/{chat_username}')).scalar()
        channel.auto_answer_text = None
        channel.is_auto_answer_enable = False

    await query.answer('✅')
