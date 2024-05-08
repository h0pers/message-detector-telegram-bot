import os

from dotenv import load_dotenv
from pyrogram import Client

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

DB_URL = conn_url = f'postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}/{os.getenv("POSTGRES_DB")}'

BOT_TOKEN = os.getenv('BOT_TOKEN')

ADMINS_ID = set([admin.strip() for admin in os.getenv('TELEGRAM_ADMIN_ID').split(',')])

TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')

TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')

TELEGRAM_CLIENT = Client("client", api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)

REDIS_PORT = os.getenv('REDIS_PORT')

REDIS_HOST = os.getenv('REDIS_HOST')


class MessageText:
    ADMIN_PANEL = 'Добро пожаловать @{username} в панели администратора!'
    ADD_CHANNEL = 'Отправьте приглашение на группу.'
    ADD_CHANNEL_SUCCESSFUL = 'Чат успешно добавлен!'
    SET_AUTO_ANSWER = 'Отправьте сообщение.'
    AUTO_ANSWER_SUCCESSFUL = 'Сообщение установлено.'
    SET_NOTIFICATION_CHAT = ('Отправьте ID чата. Для получение ID вы должны добавить бота в нужный чат, дать ему права '
                             'администратора и прописать команду /id')
    NOTIFICATION_CHAT_SUCCESSFUL = 'Чат установлен.'
    ADD_TRIGGER_WORD = 'Отправьте сообщение триггер.'
    CURRENT_TRIGGER_WORD = 'Доступные слова.'
    CURRENT_BLACKLIST_USER = 'Текущие пользователи.'
    ADD_TRIGGER_WORD_SUCCESSFUL = 'Слово успешно добавлено.'
    ADD_BLACKLIST_USER = 'Отправьте @username пользователя.'
    REMOVE_WORD = 'Выберите какое сообщение вы хотите удалить. Закончили редактировать? - /cancel'
    REMOVE_CHANNEL = 'Выберите чаты для удаление. Закончили редактировать? - /cancel'
    CONTROL_CHANNELS = 'Выберите чаты для управление.'
    CONTROL_CHANNEL = 'Сейчас редактируем ----> <b>{chat_username}</b> '
    CURRENT_OBSERVING_CHANNELS = 'Группы за которыми ведеться слежка.'
    CANCEL_SUCCESSFUL = 'Успешная отмена!'
    REPLY_SUCCESSFUL = 'Успешный ответ!'
    CALLBACK_SUCCESSFUL = 'Успешно выполнено!'
    NO_DATA = 'Ничего не найдено!'
    REPLY_TO_TRIGGERED_MESSAGE = 'Напишите ответ на сообщение.'
    TRIGGER_MESSAGE = '''
Чат: <a href="https://t.me/{chat_username}">{chat_username}</a>
Сообщение в чате: <a href="https://t.me/{chat_username}/{message_id}">Ссылка</a>
Отправитель: @{username}
➖➖➖➖➖➖➖➖➖➖

{message}
'''
