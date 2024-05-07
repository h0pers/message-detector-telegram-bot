from aiogram.types import InlineKeyboardButton

from bot.callback.admin.panel import AdminPanelCallback
from bot.keyboards.inline.main import InlineButtonText, Inline


class EditAutoAnswerInlineButtonText(InlineButtonText):
    ADD_AUTO_ANSWER = 'Установить автоответ ✒️'
    SWITCH_AUTO_ANSWER = 'Вкл/Выкл автоответ 💡'
    CLEAR_AUTO_ANSWER = 'Удалить автоответ 🚮'


add_auto_answer = InlineKeyboardButton(text=EditAutoAnswerInlineButtonText.ADD_AUTO_ANSWER,
                                       callback_data=AdminPanelCallback(ADD_AUTO_ANSWER=1).pack())

switch_auto_answer = InlineKeyboardButton(text=EditAutoAnswerInlineButtonText.SWITCH_AUTO_ANSWER,
                                          callback_data=AdminPanelCallback(SWITCH_AUTO_ANSWER=1).pack())

clear_auto_answer = InlineKeyboardButton(text=EditAutoAnswerInlineButtonText.CLEAR_AUTO_ANSWER,
                                         callback_data=AdminPanelCallback(CLEAR_AUTO_ANSWER=1).pack())

edit_auto_answer_inline_markup = Inline(
    [
        [add_auto_answer, switch_auto_answer],
        [clear_auto_answer],
    ]
)
