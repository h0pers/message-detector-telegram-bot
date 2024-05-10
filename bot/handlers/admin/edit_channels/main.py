from aiogram import Router

from .blacklist import black_list_router
from .trigger_words import trigger_words_router
from .notification_chat import notification_chat_router
from .auto_answer import auto_answer_router

edit_channel_router = Router()


def get_edit_channel_router() -> Router:
    edit_channel_routers = (black_list_router, trigger_words_router, notification_chat_router,
                            auto_answer_router)
    edit_channel_router.include_routers(*edit_channel_routers)

    return edit_channel_router
