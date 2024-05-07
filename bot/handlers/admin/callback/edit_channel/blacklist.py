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
from bot.database.models.channels import UsersBlackList, ObservingChannels
from bot.filters.state_data_has import StateDataHas
from bot.fsm.admin import AdminStates
from bot.keyboards.inline.admin.edit_blacklist import edit_blacklist_inline_markup

black_list_callback_router = Router()
callback_prefix = 'blacklist_user'


async def get_users_from_blacklist(chat_username: str) -> List[UsersBlackList]:
    chat_username = chat_username.split('@', maxsplit=1)[-1]
    async with SessionLocal.begin() as session:
        channel = (await get(session, ObservingChannels, invite_link=f'https://t.me/{chat_username}')).scalar()
        try:
            blacklists = (await get(session, UsersBlackList, channel_id=channel.id)).scalars().all()
        except AttributeError:
            return []

        return blacklists


async def get_users_from_blacklist_markup(chat_username: str) \
        -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    blacklists = await get_users_from_blacklist(chat_username)
    blacklists_count = len(blacklists)
    for blacklist_obj in blacklists:
        builder.button(text=f'@{blacklist_obj.username}', callback_data=f'{callback_prefix}{blacklist_obj.username}')

    if blacklists_count > 2:
        builder.adjust(blacklists_count // 2, blacklists_count // 2)

    return builder.as_markup()


async def add_user_to_blacklist(chat_username: str, username: str):
    chat_username = chat_username.split('@', maxsplit=1)[-1]

    async with SessionLocal.begin() as session:
        channel = (await get(session, ObservingChannels, invite_link=f'https://t.me/{chat_username}')).scalar()
        await create(session, UsersBlackList, values={'channel': channel, 'username': username})


async def delete_user_from_blacklist(chat_username: str, username: str):
    chat_username = chat_username.split('@', maxsplit=1)[-1]
    username = username.split(callback_prefix, maxsplit=1)[-1]

    async with SessionLocal.begin() as session:
        channel = (await get(session, ObservingChannels, invite_link=f'https://t.me/{chat_username}')).scalar()
        await delete(session, UsersBlackList, channel_id=channel.id, username=username)


@black_list_callback_router.callback_query(StateFilter(AdminStates.edit_chosen_channel),
                                           AdminPanelCallback.filter(F.EDIT_CHANNEL_USER_BLACKLIST == 1))
async def edit_channel_user_blacklist_handler(query: CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=edit_blacklist_inline_markup.get_markup())
    await state.set_state(AdminStates.edit_blacklist)


@black_list_callback_router.callback_query(StateFilter(AdminStates.edit_chosen_channel),
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
                                           AdminPanelCallback.filter(F.REMOVE_BLACKLIST_USER == 1),
                                           StateDataHas(['chat_username']))
async def remove_user_from_blacklist_handler(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    blacklist_markup = await get_users_from_blacklist_markup(data['chat_username'])

    if not blacklist_markup.inline_keyboard:
        await query.answer(MessageText.NO_DATA)
        return

    await query.message.edit_text(text=MessageText.ADD_BLACKLIST_USER, reply_markup=blacklist_markup)
    await state.set_state(AdminStates.remove_blacklist_user)


@black_list_callback_router.callback_query(StateFilter(AdminStates.remove_blacklist_user),
                                           F.data.startswith(callback_prefix),
                                           StateDataHas(['chat_username']))
async def remove_picked_user_handler(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await delete_user_from_blacklist(data['chat_username'], query.data)
    blacklist_markup = await get_users_from_blacklist_markup(data['chat_username'])
    await query.message.edit_reply_markup(reply_markup=blacklist_markup)


@black_list_callback_router.callback_query(StateFilter(AdminStates.edit_blacklist),
                                           AdminPanelCallback.filter(F.CURRENT_BLACKLIST == 1),
                                           StateDataHas(['chat_username']))
async def get_users_from_blacklist_handler(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    blacklist_markup = await get_users_from_blacklist_markup(data['chat_username'])

    if not blacklist_markup.inline_keyboard:
        await query.answer(MessageText.NO_DATA)
        return

    await query.message.answer(text=MessageText.CURRENT_BLACKLIST_USER, reply_markup=blacklist_markup)
    await query.answer()
