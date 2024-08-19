from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from src.bot import bot
from src.other import *
from src.config import main_handlers as logger, instr_contacts, contact_text, name_sc, add_sc

basic_router = Router()
prev_squad = -999


@basic_router.message(IsRandom(), CommandStart())
async def start_handler(message: Message):
    text = (f'*Добро пожаловать в инфо-бота летней школы МФТИ*'
            f'\nЯ могу помочь узнавать о новых событиях быстрее всего!'
            f'\nНажми на /help чтобы узнать все существующие команды')
    await message.answer(text, parse_mode='MarkDown')
    logger.info(f'/start - @{message.from_user.username} - {message.from_user.id}')


@basic_router.message(CommandStart())
async def start_handler(message: Message, command: CommandObject):
    if purpose := await link_code_check(command.args):
        text = (f'*Добро пожаловать в инфо-бота летней школы МФТИ*'
                f'\nЯ могу помочь узнавать о новых событиях быстрее всего!'
                f'\nНажми на /help чтобы узнать все существующие команды')
        if message.from_user.username:
            await link_code_join(command.args)
            await add_sc[purpose[0]](message.from_user.id, message.from_user.username)
            text = f'*Вы успешно добавлены в список {name_sc[purpose[0]]}!*\n\n' + text
            log_text = f'Joined by /start link - @{message.from_user.username} - {message.from_user.id}'
        else:
            text = (f'  *Вас не получилось добавить в список {name_sc[purpose[0]]}*'
                    f'\n_Добавьте себе username чтобы пользоваться этим ботом._')
            log_text = f'Attempt to join by /start link - !@{message.from_user.username}! - {message.from_user.id}'
    else:
        text = ('*Добро пожаловать в инфо-бота летней школы МФТИ!*'
                '\n_У вас ограниченный доступ к боту'
                '\nЧтобы получить полный доступ вам необходимо перейти по ссылке полученную от админов._')
        log_text = f'/start - unverified user - @{message.from_user.username} - {message.from_user.id}'

    await message.reply(text, parse_mode='MarkDown')
    logger.info(log_text)


@basic_router.message(IsRandom(), Command('help'))
async def help_handler(message: Message):
    text = ("*Добро пожаловать в инфо-бота летней школы МФТИ!"
            f"\nСуществующие команды этого бота:*"
            f"\n\n/start  —  Перезапуск бота"
            f"\n/help  —  Помощь"
            f"\n/contact  —  Список полезных контактов")
    if await staff_check(message.from_user.id):
        text += "\n/panel  —   Админ-панель"
    await message.reply(text, parse_mode='MarkDown')
    logger.info(f'/help - @{message.from_user.username} - {message.from_user.id}')


@basic_router.message(IsRandom(), Command('contact'))
async def contact_handler(message: Message, state: FSMContext):
    text = "Добро пожаловать в инфо-бота летней школы МФТИ!\n" + contact_text
    msg = await message.answer(text, parse_mode='MarkDown', reply_markup=instructors_keyboard)
    await state.update_data({'message_id': msg.message_id})
    logger.info(f'/contact - @{message.from_user.username} - {message.from_user.id}')


@basic_router.callback_query(IsRandom(), F.data.startswith('squad_'))
async def contact_squad_show(callback_query: CallbackQuery, state: FSMContext):
    global prev_squad  # it is a lot faster than using FSM (db)
    squad = int(callback_query.data[6:])
    if squad != prev_squad:
        prev_squad = squad
        text = f"Добро пожаловать в инфо-бота летней школы МФТИ!\n\nКонтакты вожатых {squad} отряда\n" + \
               '\n'.join('  '.join(contact) for contact in instr_contacts[squad-1]) + '\n' + contact_text
        await bot.edit_message_text(text, callback_query.from_user.id, (await state.get_data())['message_id'],
                                    reply_markup=instructors_keyboard, parse_mode='MarkDown')
    else:
        await callback_query.answer(f'Контакты для {squad} отряда уже выведены')
