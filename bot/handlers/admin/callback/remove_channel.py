from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callback.admin.panel import AdminPanelCallback
from bot.config import MessageText
from bot.database.main import SessionLocal
from bot.database.methods.delete import delete
from bot.database.models.channels import ObservingChannels
from bot.fsm.admin import AdminStates

remove_chanel_router = Router()
invite_link_validator = 'https://t.me/'


async def remove_channel(invite_link: str):
    if not invite_link.startswith(invite_link_validator):
        raise Exception(f'Invalid invite link. {invite_link}. Have to start with {invite_link_validator}')

    async with SessionLocal.begin() as session:
        await delete(session, ObservingChannels, invite_link=invite_link)


@remove_chanel_router.callback_query(StateFilter(None), AdminPanelCallback.filter(F.REMOVE_OBSERVING_CHANNEL == 1))
async def remove_channel_handler(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=MessageText.REMOVE_CHANNEL)
    await state.set_state(AdminStates.remove_channel)
    await query.answer()