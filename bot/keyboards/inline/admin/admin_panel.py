from aiogram.types import InlineKeyboardButton

from bot.callback.admin.panel import AdminPanelCallback
from bot.keyboards.inline.main import InlineButtonText, Inline


class AdminPanelInlineButtonText(InlineButtonText):
    ADD_OBSERVING_CHANNEL = 'Добавить группы ➕'
    REMOVE_OBSERVING_CHANNEL = 'Удалить группы ➖'
    EDIT_CHANNEL_TRIGGER_WORDS = 'Изменить слова ✒️'
    EDIT_CHANNEL_USER_BLACKLIST = 'Изменить черный список 📓'
    EDIT_CHANNEL_NOTIFICATION_CHAT = 'Управлять уведомлениями 📦'
    EDIT_CHANNEL_AUTO_ANSWER = 'Управлять автоответом 🕊️'
    CURRENT_OBSERVING_CHANNELS_LIST = 'Список групп 📄'


add_observing_channel = InlineKeyboardButton(text=AdminPanelInlineButtonText.ADD_OBSERVING_CHANNEL,
                                             callback_data=AdminPanelCallback(ADD_OBSERVING_CHANNEL=1).pack())

remove_observing_channel = InlineKeyboardButton(text=AdminPanelInlineButtonText.REMOVE_OBSERVING_CHANNEL,
                                                callback_data=AdminPanelCallback(REMOVE_OBSERVING_CHANNEL=1).pack())

current_observing_channels = InlineKeyboardButton(text=AdminPanelInlineButtonText.CURRENT_OBSERVING_CHANNELS_LIST,
                                                  callback_data=AdminPanelCallback(
                                                      CURRENT_OBSERVING_CHANNELS_LIST=1).pack())

edit_channel_trigger_words = InlineKeyboardButton(text=AdminPanelInlineButtonText.EDIT_CHANNEL_TRIGGER_WORDS,
                                                  callback_data=AdminPanelCallback(EDIT_CHANNEL_TRIGGER_WORDS=1).pack())

edit_channel_user_blacklist = InlineKeyboardButton(text=AdminPanelInlineButtonText.EDIT_CHANNEL_USER_BLACKLIST,
                                                   callback_data=AdminPanelCallback(
                                                       EDIT_CHANNEL_USER_BLACKLIST=1).pack())

edit_channel_auto_answer = InlineKeyboardButton(text=AdminPanelInlineButtonText.EDIT_CHANNEL_AUTO_ANSWER,
                                                callback_data=AdminPanelCallback(EDIT_CHANNEL_AUTO_ANSWER=1).pack())

edit_channel_notification_chat = InlineKeyboardButton(text=AdminPanelInlineButtonText.EDIT_CHANNEL_NOTIFICATION_CHAT,
                                                      callback_data=AdminPanelCallback(
                                                          EDIT_CHANNEL_NOTIFICATION_CHAT=1).pack())

admin_panel_inline_markup = Inline(
    [
        [add_observing_channel, remove_observing_channel],
        [edit_channel_trigger_words, edit_channel_user_blacklist],
        [edit_channel_auto_answer, edit_channel_notification_chat],
        [current_observing_channels],
    ]
)
