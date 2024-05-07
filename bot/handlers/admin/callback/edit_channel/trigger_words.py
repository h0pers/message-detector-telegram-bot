from typing import List

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from bot.callback.admin.panel import AdminPanelCallback
from bot.config import MessageText
from bot.database.main import SessionLocal
from bot.database.methods.delete import delete
from bot.database.methods.get import get
from bot.database.models.channels import ObservingChannels, TriggerWordsList
from bot.filters.state_data_has import StateDataHas
from bot.fsm.admin import AdminStates
from bot.keyboards.inline.admin.edit_trigger_words import edit_trigger_words_inline_markup

trigger_words_callback_router = Router()


async def get_trigger_words(chat_username: str) -> List[TriggerWordsList]:
    chat_username = chat_username.split('@', maxsplit=1)[-1]
    async with SessionLocal.begin() as session:
        channel = (await get(session, ObservingChannels, invite_link=f'https://t.me/{chat_username}')).scalar()
        try:
            words = (await get(session, TriggerWordsList, channel_id=channel.id)).scalars().all()
        except AttributeError:
            return []

        return words


async def get_trigger_words_markup(chat_username: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    words = await get_trigger_words(chat_username)
    words_count = len(words)

    for word_obj in words:
        builder.button(text=word_obj.word, callback_data=f'word:{word_obj.word}')
    if words_count > 2:
        builder.adjust(words_count // 2, words_count // 2)

    return builder.as_markup()


async def remove_trigger_word(word: str, chat_username: str, callback_prefix: str = 'word:'):
    word = word.split(callback_prefix, maxsplit=1)[-1]
    chat_username = chat_username.split('@', maxsplit=1)[-1]

    async with SessionLocal.begin() as session:
        channel = (await get(session, ObservingChannels, invite_link=f'https://t.me/{chat_username}')).scalar()

        await delete(session, TriggerWordsList, channel_id=channel.id, word=word)


@trigger_words_callback_router.callback_query(StateFilter(AdminStates.edit_chosen_channel),
                                              AdminPanelCallback.filter(F.EDIT_CHANNEL_TRIGGER_WORDS == 1))
async def edit_channel_trigger_words_handler(query: CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=edit_trigger_words_inline_markup.get_markup())
    await state.set_state(AdminStates.edit_trigger_words)
    await query.answer()


@trigger_words_callback_router.callback_query(StateFilter(AdminStates.edit_trigger_words),
                                              AdminPanelCallback.filter(F.ADD_TRIGGER_WORD == 1))
async def add_trigger_words_handler(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=MessageText.ADD_TRIGGER_WORD)
    await state.set_state(AdminStates.add_trigger_word)
    await query.answer()


@trigger_words_callback_router.callback_query(StateFilter(AdminStates.edit_trigger_words),
                                              AdminPanelCallback.filter(F.CURRENT_TRIGGER_WORDS == 1),
                                              StateDataHas(['chat_username']))
async def get_trigger_words_handler(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    words_markup = await get_trigger_words_markup(data['chat_username'])
    if not words_markup.inline_keyboard:
        await query.answer(MessageText.NO_DATA)
        return

    await query.message.answer(MessageText.CURRENT_TRIGGER_WORD, reply_markup=words_markup)
    await query.answer()


@trigger_words_callback_router.callback_query(StateFilter(AdminStates.edit_trigger_words),
                                              AdminPanelCallback.filter(F.REMOVE_TRIGGER_WORD == 1),
                                              StateDataHas(['chat_username']))
async def remove_trigger_words_handler(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    words_markup = await get_trigger_words_markup(data['chat_username'])
    if not words_markup.inline_keyboard:
        await query.answer(MessageText.NO_DATA)
        return

    await query.message.edit_text(MessageText.REMOVE_WORD, reply_markup=words_markup)
    await state.set_state(AdminStates.remove_trigger_words)
    await query.answer()


@trigger_words_callback_router.callback_query(StateFilter(AdminStates.remove_trigger_words),
                                              F.data.startswith('word:'),
                                              StateDataHas(['chat_username']))
async def remove_picked_word_handler(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await remove_trigger_word(query.data, data['chat_username'])

    words_markup = await get_trigger_words_markup(data['chat_username'])

    await query.message.edit_reply_markup(reply_markup=words_markup)
    await query.answer()
