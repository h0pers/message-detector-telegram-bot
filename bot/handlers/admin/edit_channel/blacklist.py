from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.filters.state_data_has import StateDataHas
from bot.fsm.admin import AdminStates
from bot.handlers.admin.callback.edit_channel.blacklist import add_user_to_blacklist

black_list_router = Router()


@black_list_router.message(StateFilter(AdminStates.add_blacklist_user),
                           F.text.startswith('@'),
                           StateDataHas(['chat_username']))
async def add_user_blacklist_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    username = message.text.split('@', maxsplit=1)[-1]

    await add_user_to_blacklist(data['chat_username'], username)
    await state.set_state(AdminStates.edit_blacklist)
