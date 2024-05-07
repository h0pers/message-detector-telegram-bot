from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery

from bot.callback.admin.triggered_message import TriggeredMessageCallback
from bot.config import ADMINS_ID, MessageText, TELEGRAM_CLIENT
from bot.filters.state_data_has import StateDataHas
from bot.filters.trigger_message import IsTriggerMessage
from bot.fsm.admin import AdminStates
from bot.handlers.admin.callback.channels_list import get_channels
from bot.handlers.admin.callback.edit_channel.blacklist import add_user_to_blacklist, delete_user_from_blacklist
from bot.keyboards.inline.admin.triggered_message import TriggeredMessageInlineButtonText
from bot.keyboards.inline.main import Inline
from bot.middleware.db_updates import CollectData, CollectCallbackData

other_router = Router()

other_router.message.middleware(CollectData())
other_router.callback_query.middleware(CollectCallbackData())


def get_block_user_inline(username: str, chat_username: str):
    callback_data = {
        'USERNAME': username,
        'CHAT_USERNAME': chat_username,
    }
    block_user = InlineKeyboardButton(text=TriggeredMessageInlineButtonText.BLOCK_USER,
                                      callback_data=TriggeredMessageCallback(**callback_data, BLOCK_USER=1).pack())
    reply_user = InlineKeyboardButton(text=TriggeredMessageInlineButtonText.REPLY_USER,
                                      callback_data=TriggeredMessageCallback(**callback_data, REPLY_USER=1).pack())

    return Inline([[block_user, reply_user]])


def get_unblock_user_inline(username: str, chat_username: str):
    callback_data = {
        'USERNAME': username,
        'CHAT_USERNAME': chat_username,
    }
    unblock_user = InlineKeyboardButton(text=TriggeredMessageInlineButtonText.UNBLOCK_USER,
                                        callback_data=TriggeredMessageCallback(**callback_data, UNBLOCK_USER=1).pack())
    reply_user = InlineKeyboardButton(text=TriggeredMessageInlineButtonText.REPLY_USER,
                                      callback_data=TriggeredMessageCallback(**callback_data, REPLY_USER=1).pack())

    return Inline([[unblock_user, reply_user]])


@other_router.message(StateFilter(AdminStates.reply_to_triggered_message),
                      F.text,
                      StateDataHas(['reply_username']))
async def reply_message_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(text=MessageText.REPLY_SUCCESSFUL)
    await TELEGRAM_CLIENT.send_message(data['reply_username'], message.text)
    await state.clear()


@other_router.message(IsTriggerMessage())
async def trigger_message_handler(message: Message, bot: Bot):
    block_user_inline = get_block_user_inline(message.from_user.username, message.chat.username)
    channel = (await get_channels(invite_link=f'https://t.me/{message.chat.username}'))[0]

    async def send_message(chat_id):
        await bot.send_message(
            text=MessageText.TRIGGER_MESSAGE.format(
                chat_username=message.chat.username,
                message_id=message.message_id,
                username=message.from_user.username,
                message=message.text,
            ),
            chat_id=chat_id,
            disable_web_page_preview=True,
            reply_markup=block_user_inline.get_markup())

    if not channel.is_auto_answer_enable:
        for admin_chat_id in ADMINS_ID:
            await send_message(admin_chat_id)
            return

    await send_message(channel.notification_chat_id)


@other_router.callback_query(TriggeredMessageCallback.filter(F.BLOCK_USER == 1))
async def block_message_handler(query: CallbackQuery, callback_data: TriggeredMessageCallback):
    unblock_inline = get_unblock_user_inline(callback_data.USERNAME, callback_data.CHAT_USERNAME)
    await add_user_to_blacklist(callback_data.CHAT_USERNAME, callback_data.USERNAME)

    await query.message.edit_reply_markup(reply_markup=unblock_inline.get_markup())
    await query.answer()


@other_router.callback_query(TriggeredMessageCallback.filter(F.UNBLOCK_USER == 1))
async def unblock_message_handler(query: CallbackQuery, callback_data: TriggeredMessageCallback):
    block_inline = get_block_user_inline(callback_data.USERNAME, callback_data.CHAT_USERNAME)
    await delete_user_from_blacklist(callback_data.CHAT_USERNAME, callback_data.USERNAME)

    await query.message.edit_reply_markup(reply_markup=block_inline.get_markup())
    await query.answer()


@other_router.callback_query(TriggeredMessageCallback.filter(F.REPLY_USER == 1))
async def reply_message_handler(query: CallbackQuery, callback_data: TriggeredMessageCallback, state: FSMContext):
    await query.message.answer(text=MessageText.REPLY_TO_TRIGGERED_MESSAGE)
    await state.set_state(AdminStates.reply_to_triggered_message)
    await state.update_data({'reply_username': callback_data.USERNAME})
    await query.answer()
