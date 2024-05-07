from typing import Tuple

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config import MessageText

from .callback.main import get_other_callback_router
from .user.main import get_user_router
from .admin.main import get_admin_router
from .other import other_router

router = Router()


@router.message(Command(commands=['cancel']))
async def cancel_handler(message: Message, state: FSMContext):
    await message.answer(text=MessageText.CANCEL_SUCCESSFUL)
    await state.clear()


def get_all_routers() -> Tuple[Router]:
    return router, get_admin_router(), get_user_router(), other_router, get_other_callback_router()
