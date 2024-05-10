from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config import MessageText
from bot.fsm.admin import AdminStates
from bot.handlers.admin.callback.edit_channel.blacklist import add_user_to_blacklist

black_list_router = Router()


@black_list_router.message(StateFilter(AdminStates.add_blacklist_user),
                           F.forward_from.id)
async def add_user_blacklist_handler(message: Message, state: FSMContext):
    await add_user_to_blacklist(telegram_id=message.forward_from.id, username=message.forward_from.username)
    await message.answer(text=MessageText.ADD_BLACKLIST_USER_SUCCESSFUL.format(
        username=message.forward_from.username or message.forward_from.id
    ))
    await state.set_state(AdminStates.edit_blacklist)
