from aiogram.filters.state import State, StatesGroup


class CommonEdit(StatesGroup):
    panel = State()
    add = State()
    method = State()
    link = State()
    mailing = State()
    mailing_message = State()
    delete = State()
