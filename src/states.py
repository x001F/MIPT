from aiogram.filters.state import State, StatesGroup


class Verification(StatesGroup):
    full_name = State()


class CommonEdit(StatesGroup):
    panel = State()
    add = State()
    delete = State()
    sure_delete = State()


class AdminEdit(StatesGroup):
    add = State()


class RatingEdit(StatesGroup):
    add = State()
    delete = State()
    sure_delete = State()


class BlockEdit(StatesGroup):
    block_user = State()
    unblock_user = State()
