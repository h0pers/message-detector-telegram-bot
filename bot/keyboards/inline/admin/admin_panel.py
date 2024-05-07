from aiogram.types import InlineKeyboardButton

from bot.callback.admin.panel import AdminPanelCallback
from bot.keyboards.inline.main import InlineButtonText, Inline


class AdminPanelInlineButtonText(InlineButtonText):
    ADD_OBSERVING_CHANNEL = 'Добавить группу ➕'
    REMOVE_OBSERVING_CHANNEL = 'Удалить группу ➖'
    CONTROL_OBSERVING_CHANNELS = 'Управлять группами 📓'
    CURRENT_OBSERVING_CHANNELS_LIST = 'Список групп 📄'


add_observing_channel = InlineKeyboardButton(text=AdminPanelInlineButtonText.ADD_OBSERVING_CHANNEL,
                                             callback_data=AdminPanelCallback(ADD_OBSERVING_CHANNEL=1).pack())

remove_observing_channel = InlineKeyboardButton(text=AdminPanelInlineButtonText.REMOVE_OBSERVING_CHANNEL,
                                                callback_data=AdminPanelCallback(REMOVE_OBSERVING_CHANNEL=1).pack())

control_observing_channels = InlineKeyboardButton(text=AdminPanelInlineButtonText.CONTROL_OBSERVING_CHANNELS,
                                                  callback_data=AdminPanelCallback(CONTROL_OBSERVING_CHANNELS=1).pack())

current_observing_channels = InlineKeyboardButton(text=AdminPanelInlineButtonText.CURRENT_OBSERVING_CHANNELS_LIST,
                                                  callback_data=AdminPanelCallback(
                                                      CURRENT_OBSERVING_CHANNELS_LIST=1).pack())

admin_panel_inline_markup = Inline(
    [
        [add_observing_channel, remove_observing_channel],
        [control_observing_channels],
        [current_observing_channels],
    ]
)
