from aiogram.types import (InlineKeyboardMarkup, ReplyKeyboardMarkup,
                           InlineKeyboardButton, KeyboardButton, KeyboardButtonRequestUsers)

panel_buttons = [
    [InlineKeyboardButton(text='Админы', callback_data='edit_admins')],
    [InlineKeyboardButton(text='Вожатые', callback_data='edit_instructors')],
    [InlineKeyboardButton(text='Ученики', callback_data='edit_students')],
    [InlineKeyboardButton(text='Рейтинг отрядов', callback_data='edit_rating')]
]

admins_edit_buttons = [
    [InlineKeyboardButton(text='Добавить админа', callback_data='add_admins')],
    [InlineKeyboardButton(text='Удалить админа', callback_data='delete_admins')],
    [InlineKeyboardButton(text='Назад', callback_data='cancel')]
]

instructors_edit_buttons = [
    [InlineKeyboardButton(text='Добавить вожатого', callback_data='add_instructors')],
    [InlineKeyboardButton(text='Удалить вожатого', callback_data='delete_instructors')],
    [InlineKeyboardButton(text='Назад', callback_data='cancel')]
]

students_edit_buttons = [
    [InlineKeyboardButton(text='Добавить ученика', callback_data='add_students')],
    [InlineKeyboardButton(text='Удалить ученика', callback_data='delete_students')],
    [InlineKeyboardButton(text='Назад', callback_data='cancel')]
]

rating_edit_buttons = [
    [InlineKeyboardButton(text='Изменить рейтинг', callback_data='add_rating')],
    [InlineKeyboardButton(text='Удалить рейтинг', callback_data='delete_rating')],
    [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
]


share_contact_buttons = [
    [KeyboardButton(text='Подать заявку', request_contact=True)]
]

share_users_buttons = [
    [KeyboardButton(text='Выбрать',
                    request_users=KeyboardButtonRequestUsers(request_id=1, user_is_bot=False, max_quantity=10))],
    [KeyboardButton(text='Отмена')]
]

unblock_move_buttons = [
    [InlineKeyboardButton(text='<', callback_data='swipe_back')],
    [InlineKeyboardButton(text='')],
    [InlineKeyboardButton(text='>', callback_data='swipe_forward')]
]

cancel_button = [
    [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
]

back_button = [
    [InlineKeyboardButton(text='Вернуться обратно к панели', callback_data='back')]
]

panel_keyboard = InlineKeyboardMarkup(inline_keyboard=panel_buttons)
admins_edit_keyboard = InlineKeyboardMarkup(inline_keyboard=admins_edit_buttons)
instructors_edit_keyboard = InlineKeyboardMarkup(inline_keyboard=instructors_edit_buttons)
students_edit_keyboard = InlineKeyboardMarkup(inline_keyboard=students_edit_buttons)
rating_edit_keyboard = InlineKeyboardMarkup(inline_keyboard=rating_edit_buttons)
share_contact_keyboard = ReplyKeyboardMarkup(keyboard=share_contact_buttons, one_time_keyboard=True)
share_users_keyboard = ReplyKeyboardMarkup(keyboard=share_users_buttons, one_time_keyboard=True)
inline_cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=cancel_button)
back_keyboard = InlineKeyboardMarkup(inline_keyboard=back_button)
