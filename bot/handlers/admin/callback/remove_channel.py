from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callback.admin.panel import AdminPanelCallback
from bot.config import MessageText
from bot.database.main import SessionLocal
from bot.database.methods.delete import delete
from bot.database.methods.get import get
from bot.database.models.channels import ObservingChannels, UsersBlackList, TriggerWordsList
from bot.fsm.admin import AdminStates
from bot.handlers.admin.callback.channels_list import get_channels_keyboard_markup

remove_chanel_router = Router()


async def remove_channel(name: str):
    async with SessionLocal.begin() as session:
        channel = (await get(session, ObservingChannels, invite_link=f'https://t.me/{name}')).scalar()
        await delete(session, UsersBlackList, channel_id=channel.id)
        await delete(session, TriggerWordsList, channel_id=channel.id)
        await delete(session, ObservingChannels, id=channel.id)


@remove_chanel_router.callback_query(StateFilter(None), AdminPanelCallback.filter(F.REMOVE_OBSERVING_CHANNEL == 1))
async def remove_channel_handler(query: CallbackQuery, state: FSMContext):
    channels_keyboard = await get_channels_keyboard_markup()
    if not channels_keyboard.inline_keyboard:
        await query.answer(MessageText.NO_DATA)
        return

    await query.message.edit_text(text=MessageText.REMOVE_CHANNEL, reply_markup=channels_keyboard)
    await state.set_state(AdminStates.remove_channel)
    await query.answer()


@remove_chanel_router.callback_query(StateFilter(AdminStates.remove_channel), F.data.startswith('@'))
async def remove_picked_channel_handler(query: CallbackQuery, state: FSMContext):
    picked_channel_username = query.data.replace('@', '')
    await remove_channel(picked_channel_username)
    channels_keyboard = await get_channels_keyboard_markup()
    await query.message.edit_reply_markup(reply_markup=channels_keyboard)
    await query.answer(MessageText.CALLBACK_SUCCESSFUL)
