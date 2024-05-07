from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.admin.callback.channels_list import get_channels
from bot.handlers.admin.callback.edit_channel.blacklist import get_users_from_blacklist
from bot.handlers.admin.callback.edit_channel.trigger_words import get_trigger_words


class IsTriggerMessage(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext, *args,
                       **kwargs):
        channels = await get_channels()
        banned_users = await get_users_from_blacklist(message.chat.username)
        trigger_word_objects = await get_trigger_words(message.chat.username)

        usernames = [channel.invite_link.split('https://t.me/', maxsplit=1)[-1] for channel in channels]
        banned_usernames = [user.username for user in banned_users]
        trigger_words = [obj.word for obj in trigger_word_objects]

        if message.chat.username not in usernames:
            return False

        if message.from_user.username in banned_usernames:
            return False

        if message.text.upper() not in [word.upper() for word in trigger_words]:
            return False

        return True
