from aiogram.filters.callback_data import CallbackData


class TriggeredMessageCallback(CallbackData, prefix="triggered_message"):
    USERNAME: str
    CHAT_USERNAME: str
    BLOCK_USER: int = 0
    UNBLOCK_USER: int = 0
    REPLY_USER: int = 0
