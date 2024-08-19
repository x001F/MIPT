from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from src.bot import bot
from src.other import *
from src.config import admin as logger, func_sc, name_sc, delete_sc
from src.states import CommonEdit

delete_router = Router()


@delete_router.callback_query(IsStaff(), F.data.startswith('delete_'), CommonEdit.panel)
async def delete_user_get(callback_query: CallbackQuery, state: FSMContext):
    users_data = await func_sc[callback_query.data[7:]]()
    name = name_sc[callback_query.data[7:]]
    if users_data:
        markup = delete_keyboard
        text = (f'Выберите id {name} для удаления'
                f"\n\n{'\n'.join(f'`{uid}`  —   @{escape_md(uname)}'
                                 for uid, uname in users_data)}"
                f'\n_Всего {len(users_data)}_'
                f'\n\n_Вы можете прислать мне id пользователей для удаления через пробел_')
        await state.update_data({'users_data': callback_query.data[7:]})
        await state.set_state(CommonEdit.delete)
    else:
        markup = back_keyboard
        text = f'_К сожалению в списке {name} для удаления не найдено ни одного человека._'
    await bot.edit_message_text(text, callback_query.from_user.id, (await state.get_data())['message_id'],
                                reply_markup=markup, parse_mode='MarkDown')


@delete_router.message(IsStaff(), CommonEdit.delete)
async def delete_user(message: Message, state: FSMContext):
    data, _user_id = await state.get_data(), message.from_user.id
    users = tuple(map(lambda _data: _data[0], await func_sc[data['users_data']]()))
    _delete_user, name = delete_sc[data['users_data']], name_sc[data['users_data']]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Продолжить', callback_data=f'delete_{data["users_data"]}')], back_button[0]])
    if len(message.text.split()) > 1:
        filtered_users, text_ids = tuple(filter(lambda _id: int(_id) != _user_id and int(_id) in users,
                                                message.text.split())), ''
        for uid in filtered_users:
            text_ids += f'\n`{uid}`'
            await _delete_user(int(uid))

        if filtered_users:
            text = f'Удалены {len(filtered_users)} пользователей{text_ids}'
            logger.info(f'/panel - {len(filtered_users)} users were deleted - '
                        f'@{message.from_user.username} - {message.from_user.id}')
        else:
            text = '_Вы прислали некорректные данные для удаления пользователей_'
            logger.info(
                f'/panel - Attempt to delete {len(filtered_users)} users - '
                f'@{message.from_user.username} - {message.from_user.id}')
    elif (message.text.isdigit() and len(message.text) == 10 and int(message.text) != _user_id
          and int(message.text) in users):
        await _delete_user(int(message.text))
        text = f'*Удален 1 пользователь*\n`{message.text}`'
        logger.info(f'/panel - {message.text} was deleted - @{message.from_user.username} - {message.from_user.id}')
    else:
        text = '_Вы прислали некорректные данные для удаления пользователей_'

    msg = await message.answer(text, reply_markup=reply_markup, parse_mode='MarkDown')
    await state.clear()
    await state.update_data({'message_id': msg.message_id})
    await state.set_state(CommonEdit.panel)


@delete_router.callback_query(IsStaff(), F.data == 'delete_all', CommonEdit.delete)
async def delete_all_users(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    _delete_user = delete_sc[data['users_data']]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Продолжить', callback_data=f'delete_{data["users_data"]}')], back_button[0]])
    await _delete_user(callback_query.from_user.id, True)
    await bot.edit_message_text('_Все пользователи успешно удалены._', callback_query.from_user.id,
                                data['message_id'], reply_markup=reply_markup, parse_mode='MarkDown')
    await state.set_state(CommonEdit.panel)
    logger.info(f'/panel - all {data["users_data"]} were deleted - '
                f'@{callback_query.from_user.username} - {callback_query.from_user.id}')
