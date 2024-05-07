from aiogram.types import InlineKeyboardButton

from bot.callback.admin.panel import AdminPanelCallback
from bot.keyboards.inline.main import InlineButtonText, Inline


class EditChannelTriggerWordsInlineButtonText(InlineButtonText):
    ADD_WORD = 'Добавить слово ➕'
    REMOVE_WORD = 'Удалить слово ➖'
    CURRENT_WORDS = 'Текущие слова 📃'


add_trigger_word = InlineKeyboardButton(text=EditChannelTriggerWordsInlineButtonText.ADD_WORD,
                                        callback_data=AdminPanelCallback(ADD_TRIGGER_WORD=1).pack())

remove_channel_trigger_words = InlineKeyboardButton(text=EditChannelTriggerWordsInlineButtonText.REMOVE_WORD,
                                                    callback_data=AdminPanelCallback(REMOVE_TRIGGER_WORD=1).pack())

current_words = InlineKeyboardButton(text=EditChannelTriggerWordsInlineButtonText.CURRENT_WORDS,
                                     callback_data=AdminPanelCallback(CURRENT_TRIGGER_WORDS=1).pack())

edit_trigger_words_inline_markup = Inline(
    [
        [add_trigger_word, remove_channel_trigger_words],
        [current_words],
    ]
)
