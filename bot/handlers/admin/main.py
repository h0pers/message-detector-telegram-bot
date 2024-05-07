from aiogram import Router

from bot.middleware.db_updates import CollectData, CollectCallbackData
from bot.filters.is_admin import OnlyAdmin, OnlyAdminCallback

from .admin_panel import admin_panel_router
from .callback.main import get_admin_callback_router
from .add_channel import add_chanel_router
from .edit_channel.main import get_edit_channel_router

admin_router = Router()

admin_router.message.filter(OnlyAdmin())
admin_router.callback_query.filter(OnlyAdminCallback())

admin_router.message.middleware(CollectData())
admin_router.callback_query.middleware(CollectCallbackData())


def get_admin_router() -> Router:
    admin_routers = (admin_panel_router, add_chanel_router,
                     get_edit_channel_router(), get_admin_callback_router(),)
    admin_router.include_routers(*admin_routers)
    return admin_router
