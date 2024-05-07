from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

from bot.callback.admin.panel import AdminPanelCallback
from bot.config import MessageText
from bot.database.main import SessionLocal
from bot.database.methods.get import get
from bot.database.models.channels import ObservingChannels

channels_list_router = Router()


async def get_channels(**kwargs):
    async with SessionLocal.begin() as session:
        channels = (await get(session, ObservingChannels, **kwargs)).scalars().all()

    return channels


async def get_channels_keyboard_markup() -> InlineKeyboardMarkup:
    async with SessionLocal.begin() as session:
        channels = await get_channels()

    channels_quantity = len(channels)
    builder = InlineKeyboardBuilder()

    for channel in channels:
        channel_username = f'@{channel.invite_link.rsplit("/", maxsplit=1)[-1]}'
        builder.button(text=channel_username, callback_data=channel_username)

    if channels_quantity > 2:
        builder.adjust(channels_quantity // 2, channels_quantity // 2)

    return builder.as_markup()


@channels_list_router.callback_query(AdminPanelCallback.filter(F.CURRENT_OBSERVING_CHANNELS_LIST == 1))
async def get_channel_list_handler(query: CallbackQuery):
    channels_keyboard = await get_channels_keyboard_markup()
    if not channels_keyboard.inline_keyboard:
        await query.answer(MessageText.NO_DATA)
        return

    await query.message.answer(text=MessageText.CURRENT_OBSERVING_CHANNELS, reply_markup=channels_keyboard)
    await query.answer()
