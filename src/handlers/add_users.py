from aiogram.types import CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from src.bot import bot
from src.other import *
from src.config import admin as logger, name_sc
from src.states import CommonEdit
from datetime import datetime as dt

add_router = Router()


@add_router.callback_query(IsStaff(), F.data.startswith('add_'), CommonEdit.panel)
async def add_by_link(callback_query: CallbackQuery, state: FSMContext):
    user_data = callback_query.data[4:]
    name = name_sc[user_data]

    if code_info := await link_code_get(user_data):
        code, ts, join_count = code_info
        datetime = dt.fromtimestamp(ts)
        text = (f'*Панель для добавления {name} по ссылке*'
                f'\n\n`https://t.me/mipt_announce_bot?start={code}`'
                f'\n_По ссылке добавлено {join_count} человек_'
                f'\n_Время создания - {str(datetime)[:19]}_')
    else:
        text = f'\n_К сожалению ссылки для добавления {name} еще нет._'

    await bot.edit_message_text(text, callback_query.from_user.id, (await state.get_data())['message_id'],
                                reply_markup=link_keyboard, parse_mode='MarkDown')
    await state.update_data({'user_data': user_data})
    await state.set_state(CommonEdit.link)


@add_router.callback_query(IsStaff(), F.data == 'new_link', CommonEdit.link)
async def new_link(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_data = data.get('user_data')
    code, datetime = make_link()
    text = (f'*Панель для добавления {name_sc[user_data]} по ссылке*'
            f'\n\n`https://t.me/mipt_announce_bot?start={code}`'
            '\n_По ссылке добавлено 0 человек_'
            f'\nВремя создания  —   {str(datetime)[:19]}')
    await bot.edit_message_text(text, callback_query.from_user.id, data['message_id'],
                                reply_markup=link_keyboard, parse_mode='MarkDown')
    await link_code_add(code, user_data, int(datetime.timestamp()))
    logger.info(f'/panel - new link was generated - '
                f'@{callback_query.from_user.username} - {callback_query.from_user.id}')
    
    
@add_router.callback_query(IsStaff(), F.data == 'delete_link', CommonEdit.link)
async def delete_link(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_data = data.get('user_data')
    name, msg_id = name_sc[user_data], data['message_id']
    text = '*Изменения успешно применены.*'
    await bot.edit_message_text(text, callback_query.from_user.id, msg_id,
                                reply_markup=back_keyboard, parse_mode='MarkDown')
    await state.clear()
    await state.update_data({'message_id': msg_id})
    await link_code_delete(user_data)
    logger.info(f'/panel - link was deleted - @{callback_query.from_user.username} - {callback_query.from_user.id}')
