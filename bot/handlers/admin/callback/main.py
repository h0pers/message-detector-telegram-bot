from aiogram import Router

from .add_channel import add_chanel_router
from .edit_channel.main import get_edit_channel_callback_router
from .remove_channel import remove_chanel_router
from .channels_list import channels_list_router
from .control_channels import control_chanel_router

admin_callback_router = Router()


def get_admin_callback_router() -> Router:
    admin_callback_routers = (add_chanel_router, remove_chanel_router, channels_list_router,
                              control_chanel_router, get_edit_channel_callback_router())
    admin_callback_router.include_routers(*admin_callback_routers)

    return admin_callback_router
