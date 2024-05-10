from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callback.admin.panel import AdminPanelCallback
from bot.config import MessageText
from bot.database.main import SessionLocal
from bot.database.methods.get import get
from bot.database.models.channels import Settings
from bot.fsm.admin import AdminStates
from bot.keyboards.inline.admin.edit_auto_answer import edit_auto_answer_inline_markup

auto_answer_callback_router = Router()


@auto_answer_callback_router.callback_query(StateFilter(None),
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
                                            AdminPanelCallback.filter(F.SWITCH_AUTO_ANSWER == 1))
async def switch_auto_answer_handler(query: CallbackQuery, state: FSMContext):
    async with SessionLocal.begin() as session:
        settings = (await get(session, Settings, id=1)).scalar()
        await state.set_state(AdminStates.edit_auto_answer)

        if settings.auto_answer_text is None:
            await query.answer('NOT SET')
            return

        settings.is_auto_answer_enable = not settings.is_auto_answer_enable

    if not settings.is_auto_answer_enable:
        await query.answer('❌')

    await query.answer('✅')


@auto_answer_callback_router.callback_query(StateFilter(AdminStates.edit_auto_answer),
                                            AdminPanelCallback.filter(F.CLEAR_AUTO_ANSWER == 1))
async def clear_auto_answer_handler(query: CallbackQuery):
    async with SessionLocal.begin() as session:
        settings = (await get(session, Settings, id=1)).scalar()
        settings.auto_answer_text = None
        settings.is_auto_answer_enable = False

    await query.answer('✅')
