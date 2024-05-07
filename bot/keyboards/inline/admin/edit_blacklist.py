from aiogram.types import InlineKeyboardButton

from bot.callback.admin.panel import AdminPanelCallback
from bot.keyboards.inline.main import InlineButtonText, Inline


class EditChannelBlacklistInlineButtonText(InlineButtonText):
    ADD_USER = 'Добавить пользователя ➕'
    REMOVE_USER = 'Удалить пользователя ➖'
    CURRENT_BLACKLIST = 'Текущие пользователи 📃'


add_blacklist_user = InlineKeyboardButton(text=EditChannelBlacklistInlineButtonText.ADD_USER,
                                          callback_data=AdminPanelCallback(ADD_BLACKLIST_USER=1).pack())

remove_blacklist_user = InlineKeyboardButton(text=EditChannelBlacklistInlineButtonText.REMOVE_USER,
                                             callback_data=AdminPanelCallback(REMOVE_BLACKLIST_USER=1).pack())

current_blacklist = InlineKeyboardButton(text=EditChannelBlacklistInlineButtonText.CURRENT_BLACKLIST,
                                         callback_data=AdminPanelCallback(CURRENT_BLACKLIST=1).pack())

edit_blacklist_inline_markup = Inline(
    [
        [add_blacklist_user, remove_blacklist_user],
        [current_blacklist],
    ]
)
