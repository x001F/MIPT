from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

panel_buttons = [
    [InlineKeyboardButton(text='Вожатые и организаторы', callback_data='edit_staff')],
    [InlineKeyboardButton(text='Ученики', callback_data='edit_students')],
    [InlineKeyboardButton(text='Рассылка', callback_data='panel_mailing')],
]

staff_edit_buttons = [
    [InlineKeyboardButton(text='Просмотреть состав', callback_data='view_staff')],
    [InlineKeyboardButton(text='Добавить вожатых и организаторов', callback_data='add_staff')],
    [InlineKeyboardButton(text='Удалить вожатых и организаторов', callback_data='delete_staff')],
    [InlineKeyboardButton(text='Вернуться обратно к панели', callback_data='back')]
]

students_edit_buttons = [
    [InlineKeyboardButton(text='Просмотреть учеников', callback_data='view_students')],
    [InlineKeyboardButton(text='Добавить ученика', callback_data='add_students')],
    [InlineKeyboardButton(text='Удалить ученика', callback_data='delete_students')],
    [InlineKeyboardButton(text='Вернуться обратно к панели', callback_data='back')]
]

mailing_buttons = [
    [InlineKeyboardButton(text='Вожатым и организаторам', callback_data='mailing_staff')],
    [InlineKeyboardButton(text='Ученикам', callback_data='mailing_students')],
    [InlineKeyboardButton(text='Всем', callback_data='mailing_all')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]
]

link_buttons = [
    [InlineKeyboardButton(text='Создать новую ссылку', callback_data='new_link')],
    [InlineKeyboardButton(text='Удалить текущую ссылку', callback_data='delete_link')],
    [InlineKeyboardButton(text='Вернуться обратно к панели', callback_data='back')]
]

delete_buttons = [
    [InlineKeyboardButton(text='Удалить все', callback_data='delete_all')],
    [InlineKeyboardButton(text='Вернуться обратно к панели', callback_data='back')]
]

# Have to be edited manually for each school shift.
instructors_buttons = [
    [InlineKeyboardButton(text='1 отряд', callback_data='squad_1')],
    [InlineKeyboardButton(text='2 отряд', callback_data='squad_2')],
    [InlineKeyboardButton(text='3 отряд', callback_data='squad_3')],
    [InlineKeyboardButton(text='4 отряд', callback_data='squad_4')],
    [InlineKeyboardButton(text='5 отряд', callback_data='squad_5')],
    [InlineKeyboardButton(text='6 отряд', callback_data='squad_6')]
]

back_button = [
    [InlineKeyboardButton(text='Вернуться обратно к панели', callback_data='back')]
]

panel_keyboard = InlineKeyboardMarkup(inline_keyboard=panel_buttons)
staff_edit_keyboard = InlineKeyboardMarkup(inline_keyboard=staff_edit_buttons)
students_edit_keyboard = InlineKeyboardMarkup(inline_keyboard=students_edit_buttons)
mailing_panel_keyboard = InlineKeyboardMarkup(inline_keyboard=mailing_buttons)
link_keyboard = InlineKeyboardMarkup(inline_keyboard=link_buttons)
delete_keyboard = InlineKeyboardMarkup(inline_keyboard=delete_buttons)
instructors_keyboard = InlineKeyboardMarkup(inline_keyboard=instructors_buttons)
back_keyboard = InlineKeyboardMarkup(inline_keyboard=back_button)
