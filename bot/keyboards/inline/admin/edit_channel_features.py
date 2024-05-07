from aiogram.types import InlineKeyboardButton

from bot.callback.admin.panel import AdminPanelCallback
from bot.keyboards.inline.main import InlineButtonText, Inline


class EditChannelFeaturesInlineButtonText(InlineButtonText):
    EDIT_CHANNEL_TRIGGER_WORDS = 'Изменить слова ✒️'
    EDIT_CHANNEL_USER_BLACKLIST = 'Изменить черный список 📓'
    EDIT_CHANNEL_NOTIFICATION_CHAT = 'Управлять уведомлениями 📦'
    EDIT_CHANNEL_AUTO_ANSWER = 'Управлять автоответом 🕊️'


edit_channel_trigger_words = InlineKeyboardButton(text=EditChannelFeaturesInlineButtonText.EDIT_CHANNEL_TRIGGER_WORDS,
                                                  callback_data=AdminPanelCallback(EDIT_CHANNEL_TRIGGER_WORDS=1).pack())

edit_channel_user_blacklist = InlineKeyboardButton(text=EditChannelFeaturesInlineButtonText.EDIT_CHANNEL_USER_BLACKLIST,
                                                   callback_data=AdminPanelCallback(
                                                       EDIT_CHANNEL_USER_BLACKLIST=1).pack())

edit_channel_auto_answer = InlineKeyboardButton(text=EditChannelFeaturesInlineButtonText.EDIT_CHANNEL_AUTO_ANSWER,
                                                callback_data=AdminPanelCallback(EDIT_CHANNEL_AUTO_ANSWER=1).pack())

edit_channel_notification_chat = InlineKeyboardButton(text=EditChannelFeaturesInlineButtonText.EDIT_CHANNEL_NOTIFICATION_CHAT,
                                                      callback_data=AdminPanelCallback(
                                                          EDIT_CHANNEL_NOTIFICATION_CHAT=1).pack())

edit_channel_inline_markup = Inline(
    [
        [edit_channel_trigger_words, edit_channel_user_blacklist],
        [edit_channel_auto_answer],
        [edit_channel_notification_chat],
    ]
)
