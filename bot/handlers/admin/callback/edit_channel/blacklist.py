from typing import List

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callback.admin.panel import AdminPanelCallback
from bot.config import MessageText
from bot.database.main import SessionLocal
from bot.database.methods.create import create
from bot.database.methods.delete import delete
from bot.database.methods.get import get
from bot.database.models.channels import UsersBlacklist
from bot.fsm.admin import AdminStates
from bot.keyboards.inline.admin.edit_blacklist import edit_blacklist_inline_markup

black_list_callback_router = Router()
callback_prefix = 'blacklist_user:'


async def get_users_from_blacklist(**kwargs) -> List[UsersBlacklist]:
    async with SessionLocal.begin() as session:
        blacklists = (await get(session, UsersBlacklist, **kwargs)).scalars().all()

        return blacklists


async def get_users_from_blacklist_markup(**kwargs) \
        -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    blacklists = await get_users_from_blacklist(**kwargs)
    blacklists_count = len(blacklists)
    for blacklist_obj in blacklists:
        text = blacklist_obj.username or str(blacklist_obj.telegram_id)
        builder.button(text=text, callback_data=f'{callback_prefix}{blacklist_obj.telegram_id}')

    if blacklists_count > 2:
        builder.adjust(blacklists_count // 2, blacklists_count // 2)

    return builder.as_markup()


async def add_user_to_blacklist(**kwargs):

    async with SessionLocal.begin() as session:
        await create(session, UsersBlacklist, values=kwargs)


async def delete_user_from_blacklist(**kwargs):
    async with SessionLocal.begin() as session:
        await delete(session, UsersBlacklist, **kwargs)


@black_list_callback_router.callback_query(StateFilter(None),
                                           AdminPanelCallback.filter(F.EDIT_CHANNEL_USER_BLACKLIST == 1))
async def edit_channel_user_blacklist_handler(query: CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=edit_blacklist_inline_markup.get_markup())
    await query.answer()
    await state.set_state(AdminStates.edit_blacklist)


@black_list_callback_router.callback_query(StateFilter(AdminStates.edit_blacklist),
                                           AdminPanelCallback.filter(F.ADD_BLACKLIST_USER == 1))
async def add_user_blacklist_handler(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=MessageText.ADD_BLACKLIST_USER)
    await query.answer()
    await state.set_state(AdminStates.add_blacklist_user)


@black_list_callback_router.callback_query(StateFilter(AdminStates.edit_blacklist),
                                           AdminPanelCallback.filter(F.REMOVE_BLACKLIST_USER == 1))
async def remove_user_from_blacklist_handler(query: CallbackQuery, state: FSMContext):
    blacklist_markup = await get_users_from_blacklist_markup()

    if not blacklist_markup.inline_keyboard:
        await query.answer(MessageText.NO_DATA)
        return

    await query.message.edit_text(text=MessageText.ADD_BLACKLIST_USER, reply_markup=blacklist_markup)
    await state.set_state(AdminStates.remove_blacklist_user)


@black_list_callback_router.callback_query(StateFilter(AdminStates.remove_blacklist_user),
                                           F.data.startswith(callback_prefix))
async def remove_picked_user_handler(query: CallbackQuery):
    telegram_id = int(query.data.split(callback_prefix, maxsplit=1)[-1])
    await delete_user_from_blacklist(telegram_id)
    blacklist_markup = await get_users_from_blacklist_markup()
    await query.message.edit_reply_markup(reply_markup=blacklist_markup)


@black_list_callback_router.callback_query(StateFilter(AdminStates.edit_blacklist),
                                           AdminPanelCallback.filter(F.CURRENT_BLACKLIST == 1))
async def get_users_from_blacklist_handler(query: CallbackQuery):
    blacklist_markup = await get_users_from_blacklist_markup()

    if not blacklist_markup.inline_keyboard:
        await query.answer(MessageText.NO_DATA)
        return

    await query.message.answer(text=MessageText.CURRENT_BLACKLIST_USER, reply_markup=blacklist_markup)
    await query.answer()
