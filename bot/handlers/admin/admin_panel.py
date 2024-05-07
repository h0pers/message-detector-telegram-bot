from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter

from bot.keyboards.inline.admin.admin_panel import admin_panel_inline_markup

admin_panel_router = Router()


@admin_panel_router.message(StateFilter(None), Command(commands=['admin', 'start']))
async def admin_panel_handler(message: Message):
    await message.answer(text='admin panel', reply_markup=admin_panel_inline_markup.get_markup())
