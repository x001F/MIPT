import logging.handlers
from src.other import (get_staff, get_students, add_staff, add_student, delete_staff,
                       delete_student, staff_edit_keyboard, students_edit_keyboard)
from aiogram.types import BotCommand

# Startup START
BOT_TOKEN = '6857583661:AAFPeGhtnR8dIlCivwGqZ3i97WcH9c5RRok'

commands = [
    BotCommand(command='start', description='Перезапускает бота'),
    BotCommand(command='help', description='Помощь'),
    BotCommand(command='contact', description='Список полезных контактов'),
    BotCommand(command='panel', description='Админ-панель')
]
# Startup END

# Logging START
formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(funcName)s | %(name)s | %(message)s')

console = logging.StreamHandler()
console.setFormatter(formatter)

file = logging.handlers.TimedRotatingFileHandler(
    filename='src/logs/logfile', when='m', interval=1, backupCount=7, encoding='utf-8',
)
file.setFormatter(formatter)
file.suffix = '-%Y-%m-%d_%H-%M.log'

admin = logging.getLogger('admin')
admin.setLevel(logging.INFO)
admin.addHandler(console)
admin.addHandler(file)

main = logging.getLogger('main')
main.setLevel(logging.INFO)
main.addHandler(console)
main.addHandler(file)

main_handlers = logging.getLogger('main.handlers')
main_handlers.setLevel(logging.INFO)
main_handlers.addHandler(console)
main_handlers.addHandler(file)
main_handlers.propagate = False
# Logging END

# Handlers START
func_sc = {
    'staff': get_staff,
    'students': get_students,
    'edit_staff': staff_edit_keyboard,
    'edit_students': students_edit_keyboard
}
add_sc = {
    'staff': add_staff,
    'students': add_student
}
delete_sc = {
    'staff': delete_staff,
    'students': delete_student,
}
name_sc = {
    'staff': 'вожатых и организаторов',
    'students': 'учеников'
}

instr_contacts = (
    (('', ''), ('', '')),
    (('', ''), ('', '')),
    (('', ''), ('', '')),
    (('', ''), ('', '')),
    (('', ''), ('', '')),
    (('', ''), ('', ''))
)

contact_text = ("\n*Контакты для экстренной связи:*"
                "\n_Скорая помощь_           112"
                "\n*Главный организатор:*"
                "\n_<name>_ <phone number>"
                "\n*Ответственный за обучение:*"
                "\n_<name>_ {phone number}"
                "\n*Ответственный за проживание:*"
                "\n_<name>_ {phone number}"
                "\n\n_Нажми на кнопку с именем отряда чтобы получить контакты его вожатых_"
                )
# Handlers END
