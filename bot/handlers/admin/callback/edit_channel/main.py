from aiogram import Router

from .blacklist import black_list_callback_router
from .trigger_words import trigger_words_callback_router
from .notification_chat import notification_chat_callback_router
from .auto_answer import auto_answer_callback_router

edit_channel_callback_router = Router()


def get_edit_channel_callback_router() -> Router:
    edit_channel_callback_routers = (black_list_callback_router, trigger_words_callback_router,
                                     notification_chat_callback_router, auto_answer_callback_router)
    edit_channel_callback_router.include_routers(*edit_channel_callback_routers)

    return edit_channel_callback_router
