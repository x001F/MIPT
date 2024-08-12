from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from src.other.db import stuff_check, student_check
from src.other import IsNotRandom, IsNotBlocked, get_students, get_rating, share_contact_keyboard
from src.config.get_logger import *
from src.states import Verification

logger = get_logger('main.handlers')
basic_router = Router()


@basic_router.message(IsNotBlocked(), CommandStart())
async def start_handler(message: Message):
    text = f"""Добро пожаловать в инфо-бота летней школы МФТИ."""
    await message.reply(text)
    logger.info(f'/start - @{message.from_user.username} - {message.from_user.id}')


@basic_router.message(IsNotBlocked(), Command('help'))
async def help_handler(message: Message):
    text = (f"Привет, _{message.from_user.first_name}_!"
            f"\n*Существующие команды этого бота:*"
            f"\n\n/start  —  Перезапуск бота"
            f"\n/help  —  Помощь")
    if await stuff_check(message.from_user.id):
        text += ("\n/contact  —  Список полезных контактов"
                 "\n/rating  —  Рейтинг отрядов по количеству кварков"
                 "\n/panel  —   Админ-панель")
    elif await student_check(message.from_user.id):
        text += ("\n/contact  —  Список полезных контактов"
                 "\n/rating  —  Рейтинг отрядов по количеству кварков")
    else:
        text += "\n/verify  —  Подать заявку на вступление в лагерь"

    await message.answer(text, parse_mode='MarkDown')
    logger.info(f'/help - @{message.from_user.username} - {message.from_user.id}')


@basic_router.message(IsNotBlocked(), Command('verify'))
async def verify_handler(message: Message) -> None:
    text = ('Чтобы пользоваться всеми возможностями бота вам необходимо подать заявку на вступление\n'
            'Нажмите кнопку снизу чтобы подать заявку на вступление')
    await message.answer(text, reply_markup=share_contact_keyboard)

# text = ('Ваша заявка на вступление успешно подана'
#                 'Модераторы рассмотрят ее в скором времени.')


@basic_router.message(IsNotBlocked(), F.content_type == 'contact')
async def ask_full_name(message: Message, state: FSMContext) -> None:
    if message.from_user.id == message.contact.user_id:
        await message.answer('Номер телефона получен, для подачи заявки вам будет необходимо отправить свое ФИО')
        await state.set_state(Verification.full_name)
        await state.update_data({'phone_number': message.contact.phone_number})
    else:
        await message.answer('Некорректные вводимые данные, поделитесь своим контактом.',
                             reply_markup=share_contact_keyboard)


# @basic_router.message(IsNotBlocked(), F.content_type == 'text', not F.text.isascii(), Verification.full_name)
# async def ask_full_name(message: Message, state: FSMContext) -> None:
#     data = await state.get_data()
#     full_name, phone_number = message.text, data['phone_number']
    

@basic_router.message(IsNotRandom, Command('contact'))
async def contact_handler(message: Message):
    text = ''
    user_data = await get_students(message.from_user.id)
    if user_data[0]:
        text += f"*Твой отряд: №{user_data[0]}*\n"

    text = (f"{text}"
            "\n*Контакты для экстренной связи:*"
            "\n_Скорая помощь_           112"
            "\n\n*Главный организатор:*"
            "\n_Ксения_          +7 999 095-34-08"
            "\n\n*Ответственный за обучение:*"
            "\n_Елизавета_    +7 921 180-47-39"
            "\n\n*Ответственный за проживание:*"
            "\n_Анжела_         +7 937 317-02-95"
            "\n\n_Если нужной для тебя информации не нашлось, обратись к вожатым._")
    await message.reply(text, parse_mode='MarkDown')
    logger.info(f'/contact - @{message.from_user.username} - {message.from_user.id}')


@basic_router.message(IsNotRandom(), Command('rating'))
async def rating_handler(message: Message) -> None:
    rating = await get_rating()
    if rating:
        rating = '\n'.join(f'*Отряд №{team_id:< 4}*    —    *{quark_count}*' for team_id, quark_count in rating)
    else:
        rating = '*К сожалению, здесь пусто...*'
    await message.answer(f"""*Рейтинг отрядов*\n\n{rating}
    \n_Если заметили неточность или ошибку сообщите своим вожатым, они скоро все исправят._""", parse_mode='MarkDown')
    logger.info(f'/rating - @{message.from_user.username} - {message.from_user.id}')
