from aiogram.filters.callback_data import CallbackData


class AdminPanelCallback(CallbackData, prefix="admin_panel"):
    ADD_OBSERVING_CHANNEL: int = 0
    REMOVE_OBSERVING_CHANNEL: int = 0
    CONTROL_OBSERVING_CHANNELS: int = 0
    CURRENT_OBSERVING_CHANNELS_LIST: int = 0
    CLEAR_AUTO_ANSWER: int = 0
    EDIT_CHANNEL_TRIGGER_WORDS: int = 0
    EDIT_CHANNEL_USER_BLACKLIST: int = 0
    EDIT_CHANNEL_AUTO_ANSWER: int = 0
    EDIT_CHANNEL_NOTIFICATION_CHAT: int = 0
    ADD_BLACKLIST_USER: int = 0
    ADD_AUTO_ANSWER: int = 0
    SWITCH_AUTO_ANSWER: int = 0
    REMOVE_BLACKLIST_USER: int = 0
    CURRENT_BLACKLIST: int = 0
    ADD_TRIGGER_WORD: int = 0
    REMOVE_TRIGGER_WORD: int = 0
    CURRENT_TRIGGER_WORDS: int = 0
