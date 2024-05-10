from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from pyrogram import Client
from pyrogram.types import Message as ClientMessage

from bot.callback.admin.triggered_message import TriggeredMessageCallback
from bot.config import ADMINS_ID, MessageText, BOT_TOKEN
from bot.database.main import SessionLocal
from bot.database.methods.get import get
from bot.database.models.channels import Settings
from bot.handlers.admin.callback.edit_channel.blacklist import add_user_to_blacklist, delete_user_from_blacklist
from bot.keyboards.inline.admin.triggered_message import TriggeredMessageInlineButtonText
from bot.keyboards.inline.main import Inline
from bot.middleware.db_updates import CollectData, CollectCallbackData

other_router = Router()

other_router.message.middleware(CollectData())
other_router.callback_query.middleware(CollectCallbackData())


def get_block_user_inline(telegram_id: int):
    block_user = InlineKeyboardButton(text=TriggeredMessageInlineButtonText.BLOCK_USER,
                                      callback_data=TriggeredMessageCallback(TELEGRAM_ID=telegram_id, BLOCK_USER=1).pack())

    return Inline([[block_user]])


def get_unblock_user_inline(telegram_id: int):
    unblock_user = InlineKeyboardButton(text=TriggeredMessageInlineButtonText.UNBLOCK_USER,
                                        callback_data=TriggeredMessageCallback(TELEGRAM_ID=telegram_id, UNBLOCK_USER=1).pack())

    return Inline([[unblock_user]])


async def trigger_message_handler(client: Client, message: ClientMessage):
    print(message)
    telegram_id = message.from_user.id
    chat_username = message.chat.username or 'Приватный'
    username = message.from_user.username or 'Нету'
    chat_title = message.chat.title
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name or 'Нету'
    text = message.text
    message = await client.get_messages(message.chat.id, message.id)
    block_user_inline = get_block_user_inline(telegram_id)

    async with SessionLocal.begin() as session:
        settings = (await get(session, Settings, id=1)).scalar()

    async def send_message(chat_id):
        await Bot(BOT_TOKEN, parse_mode=ParseMode.HTML).send_message(
            text=MessageText.TRIGGER_MESSAGE.format(
                chat_title=chat_title,
                chat_username=chat_username,
                message_id=message.id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                telegram_id=telegram_id,
                message=text,
            ),
            chat_id=chat_id,
            disable_web_page_preview=True,
            reply_markup=block_user_inline.get_markup())

    if settings.is_auto_answer_enable:
        await client.send_message(username, settings.auto_answer_text)

    if not settings.notification_chat_id:
        for admin_chat_id in ADMINS_ID:
            await send_message(admin_chat_id)
            # try:
            #     await send_message(admin_chat_id)
            # except TelegramBadRequest:
            #     pass
        return

    await send_message(await send_message(settings.notification_chat_id))


@other_router.callback_query(TriggeredMessageCallback.filter(F.BLOCK_USER == 1))
async def block_message_handler(query: CallbackQuery, callback_data: TriggeredMessageCallback):
    unblock_inline = get_unblock_user_inline(callback_data.TELEGRAM_ID)
    await add_user_to_blacklist(telegram_id=callback_data.TELEGRAM_ID)

    await query.message.edit_reply_markup(reply_markup=unblock_inline.get_markup())
    await query.answer()


@other_router.callback_query(TriggeredMessageCallback.filter(F.UNBLOCK_USER == 1))
async def unblock_message_handler(query: CallbackQuery, callback_data: TriggeredMessageCallback):
    block_inline = get_block_user_inline(callback_data.TELEGRAM_ID)
    await delete_user_from_blacklist(telegram_id=callback_data.TELEGRAM_ID)

    await query.message.edit_reply_markup(reply_markup=block_inline.get_markup())
    await query.answer()
