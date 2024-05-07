from aiogram import Router

from bot.middleware.db_updates import CollectData
from .callback.main import get_user_callback_router
from .get_id import get_id_router

user_router = Router()

user_router.message.middleware(CollectData())


def get_user_router() -> Router:
    user_routers = (get_user_callback_router(), get_id_router)
    user_router.include_routers(*user_routers)

    return user_router
