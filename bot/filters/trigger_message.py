from pyrogram import filters
from pyrogram.types import Message

from bot.handlers.admin.callback.channels_list import get_channels
from bot.handlers.admin.callback.edit_channel.blacklist import get_users_from_blacklist
from bot.handlers.admin.callback.edit_channel.trigger_words import get_trigger_words


async def func(_, __, message: Message):
    channels = await get_channels()
    banned_users = await get_users_from_blacklist(telegram_id=message.from_user.id)
    trigger_word_objects = await get_trigger_words()

    usernames = [channel.invite_link.split('https://t.me/', maxsplit=1)[-1] for channel in channels]
    banned_users = [user.telegram_id for user in banned_users]
    trigger_words = [obj.word.lower() for obj in trigger_word_objects]
    print(usernames)
    print(banned_users)
    print(trigger_words)

    if message.chat.username not in usernames:
        return False

    if message.from_user.id in banned_users:
        return False

    if not any(word in trigger_words for word in message.text.lower().split(' ')):
        return False

    return True


is_trigger_message = filters.create(func)
