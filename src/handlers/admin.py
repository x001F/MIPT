from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from src.bot import bot
from src.other import *
from src.config import get_logger
from src.states import *
from datetime import datetime as dt

logger = get_logger('admin')
admin_router = Router()

panel_shortcut = {
    'edit_admins': admins_edit_keyboard,
    'edit_instructors': instructors_edit_keyboard,
    'edit_students': students_edit_keyboard,
    'edit_rating': rating_edit_keyboard,
}

delete_shortcut = {
    ''
}

adding_shortcut = {'add_rating': RatingEdit.add}

name_shortcut = {
    'add_admins': 'админов',
    'add_instructors': 'вожатых',
    'add_students': 'учеников'
}


@admin_router.message(IsAdmin(), Command('panel'))
async def panel_handler(message: Message, state: FSMContext) -> None:
    msg = await message.answer(f"""Добро пожаловать в админ панель.
Выберите пункт для изменения""", reply_markup=panel_keyboard)
    await state.update_data({'message_id': msg.message_id})
    logger.info(f'/panel - @{message.from_user.username} - {message.from_user.id}')


@admin_router.callback_query(IsAdmin(), F.data.startswith('edit_'))
async def edit_panel(callback_query: CallbackQuery, state: FSMContext) -> None:
    keyboard = panel_shortcut[callback_query.data]
    msg_id = (await state.get_data()).get('message_id')
    await bot.edit_message_text('Выберите действие', callback_query.from_user.id, msg_id,
                                reply_markup=keyboard)
    await state.set_state(CommonEdit.panel)


@admin_router.callback_query(IsAdmin(), lambda c: c.data in ('add_admins', 'add_instructors', 'add_students'),
                             CommonEdit.panel)
async def edit_records(callback_query: CallbackQuery, state: FSMContext) -> None:
    msg_id = (await state.get_data()).get('message_id')
    await bot.delete_message(callback_query.from_user.id, msg_id)
    text = \
        "Выберите пользователей для добавления\n" \
        "\n_ВНИМАНИЕ Для успешного добавления, пользователь должен был написать боту хотя бы раз за последние 7 дней._"
    msg = await bot.send_message(callback_query.from_user.id, text,
                                 reply_markup=share_users_keyboard, parse_mode='MarkDown')
    await state.update_data({'message_id': msg.message_id, 'cq_data': callback_query.data})
    await state.set_state(adding_shortcut.get(callback_query.data, CommonEdit.add))


@admin_router.callback_query(IsAdmin(), F.data == 'add_rating', CommonEdit.panel)
async def get_records_to_add(callback_query: CallbackQuery, state: FSMContext):
    text = 'Отправь рейтинг отрядов в формате\n_<Номер отряда> - <Количество кварков отряда>_'
    msg_id = (await state.get_data()).get('message_id')
    await bot.edit_message_text(text, callback_query.from_user.id, msg_id,
                                reply_markup=inline_cancel_keyboard, parse_mode='MarkDown')
    await state.set_state(adding_shortcut.get(callback_query.data))


@admin_router.message(IsAdmin(), F.content_type == 'users_shared', CommonEdit.add)
async def apply_adding_records(message: Message, state: FSMContext):
    ids = message.users_shared.user_ids
    data = await state.get_data()
    for uid in ids:
        student_data = await get_students(uid)

    _name = f'{len(ids)} человека' if str(len(ids))[-1] == '1' else f'{len(ids)} человек'
    text = f'_Вы добавили {_name} в список {name_shortcut.get(data.get('cq_data'))} школы._'
    msg = await message.answer(text, reply_markup=back_keyboard, parse_mode='MarkDown')
    await state.clear()
    await state.update_data({'message_id': msg.message_id})
    logger.info(f'{data.get('cq_data')[4:].title()} have been edited by - '
                f'@{message.from_user.username} - {message.from_user.id}')


@admin_router.message(IsAdmin(), F.content_type == 'text', RatingEdit.add)
async def apply_add_rating_changes(message: Message, state: FSMContext):
    await message.delete()
    text, edited_rating = '_Добавлены следующие изменения_', []
    for line in message.text.split('\n'):
        values = line.split(' - ')
        if len(values) > 1:
            print(values)
            team_id, quark_count = values
            text += f'\n*Отряд №{team_id}  —  {quark_count}*'
            if team_data := await get_rating(team_id):
                last_quark_count = team_data[0][1]
                if last_quark_count == int(quark_count):
                    continue
                text += f'*, было {last_quark_count}*'
            edited_rating.append((int(team_id), int(quark_count)))
    else:
        if edited_rating:
            await edit_rating(edited_rating)
        else:
            text = '_Вы прислали некорректные данные для того чтобы изменить рейтинг отрядов_'
        msg_id = (await state.get_data()).get('message_id')
        await bot.edit_message_text(text, message.from_user.id, msg_id,
                                    reply_markup=back_keyboard, parse_mode='MarkDown')
        await state.clear()
        await state.update_data({'message_id': msg_id})
        logger.info(f'Rating have been edited by - @{message.from_user.username} - {message.from_user.id}')


@admin_router.callback_query(IsAdmin(), lambda c: c.data in ('delete_admins', 'delete_instructors', 'delete_students'),
                             CommonEdit.panel)
async def choose_records_removal(callback_query: CallbackQuery, state: FSMContext) -> None:
    _name = name_shortcut.get(callback_query.data[7:])
    text = f'Введите @username пользователя, например (@Durov), или его идентификатор если у него нет @username'
    msg_id = (await state.get_data()).get('message_id')
    await bot.edit_message_text(text, callback_query.from_user.id, msg_id, reply_markup=inline_cancel_keyboard)
    await state.set_state(CommonEdit.delete)


@admin_router.message(IsAdmin(), F.content_type == 'text', CommonEdit.delete)
async def get_user_data(message: Message, state: FSMContext) -> None:
    user_data = message.text
    if user_data.startswith('@'):
        ...


@admin_router.callback_query(IsAdmin(), F.data == 'delete_rating',
                             CommonEdit.panel)
async def choose_rating_records_removal(callback_query: CallbackQuery, state: FSMContext) -> None:
    rating = await get_rating()
    if rating:
        rating_buttons = [
            [InlineKeyboardButton(text=f'Отряд №{team_id}', callback_data=f'rating_{team_id}')]
            for team_id, quark_count in rating
        ] + [[InlineKeyboardButton(text='Удалить всё', callback_data='rating_entire')] + cancel_button[0]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=rating_buttons)
        text = 'Выберите записи отряда для удаления'
    else:
        keyboard = inline_cancel_keyboard
        text = '_К сожалению записей рейтинга отрядов не найдено._'
    msg_id = (await state.get_data()).get('message_id')
    await bot.edit_message_text(text, callback_query.from_user.id, msg_id, reply_markup=keyboard, parse_mode='MarkDown')
    await state.set_state(RatingEdit.delete)


@admin_router.callback_query(IsAdmin(), F.data.startswith('rating_'), RatingEdit.delete)
async def ask_rating_removal_certainty(callback_query: CallbackQuery, state: FSMContext) -> None:
    team_value = callback_query.data[7:]
    if team_value != 'entire':
        quark_count = (await get_rating(int(team_value)))[0][1]
        text = (f'Удалить записи рейтинга отряда №{team_value}?'
                f'\nКоличество кварков отряда №{team_value} — {quark_count}')
    else:
        rating = await get_rating()
        text = (f'Удалить записи рейтинга всех отрядов?'
                f'\n\n*Записи рейтинга отрядов*')
        for team_id, quark_count in rating:
            text += f'*Отряд №{team_id:< 4}*    —    *{quark_count}*\n'
    msg_id = (await state.get_data()).get('message_id')
    await bot.edit_message_text(text, callback_query.from_user.id, msg_id,
                                reply_markup=back_keyboard, parse_mode='MarkDown')
    await state.update_data({'team_value': team_value})
    await state.set_state(RatingEdit.sure_delete)


@admin_router.callback_query(IsAdmin(), F.data == 'sure_delete', RatingEdit.sure_delete)
async def apply_rating_removal(callback_query: CallbackQuery, state: FSMContext) -> None:
    text = '*Изменения успешно внесены.*'
    data = await state.get_data()
    msg_id, team_value = data['message_id'], data['team_value']
    await bot.edit_message_text(text, callback_query.from_user.id, msg_id,
                                reply_markup=back_keyboard, parse_mode='MarkDown')
    if team_value == 'entire':
        await delete_rating(entire=True)
        log_info = 'Entire'
    else:
        await delete_rating(team_id=team_value)
        log_info = f'Team №{team_value}'
    logger.info(f'{log_info} rating have been deleted by - '
                f'@{callback_query.from_user.username} - {callback_query.from_user.id}')


@admin_router.message(IsAdmin(), Command('block'))
async def block_handler(message: Message, state: FSMContext):
    await message.answer('Выберите пользователей для блокировки использования бота',
                         reply_markup=share_users_keyboard)
    await state.set_state(BlockEdit.block_user)


@admin_router.message(IsAdmin(), F.content_type == 'users_shared', BlockEdit.block_user)
async def apply_block(message: Message, state: FSMContext):
    ids = message.users_shared.user_ids
    timestamp = int(dt.now().timestamp())
    for uid in ids:
        await delete(uid)
        await block(uid, timestamp)

    msg = await message.answer('_Вы успешно заблокировали 10 пользователей_',
                               reply_markup=back_keyboard, parse_mode='MarkDown')
    await state.clear()
    await state.update_data({'message_id': msg.message_id})
    
    
@admin_router.message(IsAdmin(), Command('unblock'))
async def unblock_handler(message: Message, state: FSMContext):
    black_list = await get_blacklist()
    if black_list:
        text = 'Выберите пользователей для разблокировки использования бота'
        if len(black_list) <= 10:
            buttons = [
                [InlineKeyboardButton(text=str(dt.fromtimestamp(timestamp)), callback_data=f'unblock_{uid}')]
                for uid, timestamp in black_list
            ]
        else:
            ...
        # TODO
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await state.set_state(BlockEdit.unblock_user)
    else:
        text = '_К счастью к черном списке бота еще никого нет!_'
        keyboard = back_keyboard

    await message.answer(text, reply_markup=keyboard, parse_mode='MarkDown')


@admin_router.message(IsAdmin(), F.content_type == 'text', F.text == 'Отмена')
async def cancel_handler(message: Message, state: FSMContext):
    await message.delete()
    msg_id = (await state.get_data()).get('message_id')
    if msg_id:
        await bot.delete_message(message.chat.id, msg_id)
    msg = await message.answer(f"""Добро пожаловать в админ панель.
Выберите пункт для изменения""", reply_markup=panel_keyboard)
    await state.clear()
    await state.update_data({'message_id': msg.message_id})


@admin_router.callback_query(IsAdmin(), lambda cq: cq.data in ('cancel', 'back'))
async def cancel_button_press(callback_query: CallbackQuery, state: FSMContext):
    msg_id = (await state.get_data()).get('message_id')
    await bot.edit_message_text(f"""Добро пожаловать в админ панель.
Выберите пункт для изменения""", callback_query.from_user.id, msg_id, reply_markup=panel_keyboard)
    await state.clear()
    await state.update_data({'message_id': msg_id})
