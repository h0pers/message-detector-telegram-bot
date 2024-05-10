from aiogram.filters.callback_data import CallbackData


class TriggeredMessageCallback(CallbackData, prefix="triggered_message"):
    TELEGRAM_ID: int
    BLOCK_USER: int = 0
    UNBLOCK_USER: int = 0
    REPLY_USER: int = 0
