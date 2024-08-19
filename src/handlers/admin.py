from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from src.bot import bot
from src.other import *
from src.config import admin as logger, func_sc, name_sc
from src.states import CommonEdit

admin_router = Router()


@admin_router.message(IsStaff(), Command('panel'))
async def panel_handler(message: Message, state: FSMContext):
    msg = await message.answer('*Добро пожаловать в админ-панель*\nВыберите пункт для изменения',
                               reply_markup=panel_keyboard, parse_mode='MarkDown')
    await state.update_data({'message_id': msg.message_id})
    logger.info(f'/panel - @{message.from_user.username} - {message.from_user.id}')


@admin_router.message(IsStudent(), Command('panel'))
async def panel_handler(message: Message):
    await message.answer('_У вас не достаточно прав на совершение этой операции._', parse_mode='MarkDown')


@admin_router.callback_query(IsStaff(), F.data.startswith('edit_'))
async def edit_panel(callback_query: CallbackQuery, state: FSMContext):
    keyboard = func_sc[callback_query.data]
    await bot.edit_message_text('*Выберите действие*', callback_query.from_user.id,
                                (await state.get_data())['message_id'], reply_markup=keyboard, parse_mode='MarkDown')
    await state.set_state(CommonEdit.panel)


@admin_router.callback_query(IsStaff(), F.data.startswith('view_'), CommonEdit.panel)
async def view_users(callback_query: CallbackQuery, state: FSMContext):
    get_users_data, name = func_sc[callback_query.data[5:]], name_sc[callback_query.data[5:]]
    users_data = await get_users_data()

    if users_data:
        text_ids = '\n'.join(f'`{uid}`  -  @{escape_md(uname)}' for uid, uname in users_data)
        text = f'*Здесь вы можете просмотреть всех {name} летней школы МФТИ*\n\n' + \
               text_ids + f'\n_Всего {len(users_data)}_'
    else:
        text = f'_К сожалению в списке {name} еще никого нет._'

    await bot.edit_message_text(text, callback_query.from_user.id, (await state.get_data())['message_id'],
                                reply_markup=back_keyboard, parse_mode='MarkDown')
    logger.info(f'/panel - view {callback_query.data[5:]} - '
                f'@{callback_query.from_user.username} - {callback_query.from_user.id}')


@admin_router.callback_query(IsStaff(), F.data == 'panel_mailing')
async def mailing_panel(callback_query: CallbackQuery, state: FSMContext):
    msg_id = (await state.get_data())['message_id']
    await bot.edit_message_text('*Выберите получателей сообщения*', callback_query.from_user.id, msg_id,
                                reply_markup=mailing_panel_keyboard, parse_mode='MarkDown')
    await state.set_state(CommonEdit.mailing)


@admin_router.callback_query(IsStaff(), F.data.startswith('mailing_'), CommonEdit.mailing)
async def mailing_recipient_get(callback_query: CallbackQuery, state: FSMContext):
    msg_id = (await state.get_data())['message_id']
    await bot.edit_message_text('*Пришлите сообщение для пересылки*', callback_query.from_user.id, msg_id,
                                reply_markup=back_keyboard, parse_mode='MarkDown')
    await state.update_data({'users_to_mail': callback_query.data[8:]})
    await state.set_state(CommonEdit.mailing_message)


@admin_router.message(IsStaff(), CommonEdit.mailing_message)
async def mailing_message_get(message: Message, state: FSMContext):
    users, _user_id = (await func_sc.get((await state.get_data())['users_to_mail'], get_users)(),
                       message.from_user.id)
    for uid, uname in users:
        if _user_id != int(uid):
            await message.forward(uid)

    user_count = len(users) - 1 if len(users) != 0 else len(users)
    msg = await message.answer(f'_Сообщение успешно отправлено {user_count} пользователям_',
                               reply_markup=back_keyboard, parse_mode='MarkDown')
    await state.update_data({'message_id': msg.message_id})
    logger.info(f'/panel - mailing to {user_count} users - @{message.from_user.username} - {message.from_user.id}')


@admin_router.callback_query(IsStaff(), F.data == 'back')
async def cancel_button_press(callback_query: CallbackQuery, state: FSMContext):
    msg_id = (await state.get_data())['message_id']
    if callback_query.message.message_id == msg_id:
        await bot.edit_message_text('*Добро пожаловать в админ-панель*\nВыберите пункт для изменения',
                                    callback_query.from_user.id, msg_id, reply_markup=panel_keyboard,
                                    parse_mode='MarkDown')
        await state.clear()
        await state.update_data({'message_id': msg_id})
