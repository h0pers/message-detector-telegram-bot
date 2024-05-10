from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    add_channel = State()
    edit_auto_answer = State()
    add_auto_answer = State()
    edit_notification_chat = State()
    remove_channel = State()
    control_channels = State()
    edit_chosen_channel = State()
    edit_trigger_words = State()
    remove_trigger_words = State()
    add_trigger_word = State()
    edit_blacklist = State()
    remove_blacklist_user = State()
    add_blacklist_user = State()
