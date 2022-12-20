from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage




bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

bot.set_my_commands([
    types.BotCommand("/start", "Начать работу"),
    types.BotCommand("/help", "Памагити"),
    types.BotCommand("/ban", "Забанить пользователя(нужно ответить на его сообщение), доступно только админам"),
    types.BotCommand("/unban", "Разбанить пользователя(нужно ответить на его сообщение), доступно только админам"),
    types.BotCommand("/promote", "Сделать пользователя админом(нужно ответить на его сообщение), доступно только админам"),
    types.BotCommand("/statistics", "Получить стастистику"),
    types.BotCommand("/leave", "Заставить бота уйти из чата")
])


@dp.message_handler(commands=['help'])
async def help(message):
    await bot.send_message(message.chat.id, 'Вот что я умею: \n'+
                                      '1) Помогать админиминистратором банить/разбанить/сделать админом человека\n' +
                                      '2) Получить статистику по чату\n' +
                                       '3) Уйти из чата(\n' +
                                       '4) Приветствовать новых участников\n')


@dp.message_handler(commands=['start'])
async def start_message(message):
    await bot.send_message(message.chat.id, f'Привет! Я могу помочь с администрированием группы.')


@dp.message_handler(commands=['ban'])
async def ban(message):
    is_not_creator = (await bot.get_chat_member(message.chat.id, message.from_user.id)).status != "creator"
    is_administrator = (await bot.get_chat_member(message.chat.id, message.from_user.id)).status == "administrator"
    if (is_not_creator and not is_administrator) or (is_administrator and (
    await bot.get_chat_member(message.chat.id, message.from_user.id)).can_restrict_members != True):
        await bot.send_message(message.chat.id,
                         f'{message.from_user.username}, у вас нет прав для совершения действия!')
        return
    if message.reply_to_message is not None:
        user_id_to_ban = message.reply_to_message.from_user.id
        if (await bot.get_chat_member(message.chat.id, user_id_to_ban)).status in ["creator", "administrator"]:
            await bot.send_message(message.chat.id, f'Вы не можете заблокировать администратора или владельца чата!')
            return
        if user_id_to_ban == (await bot.me).id:
            await bot.send_message(message.chat.id, f'Не могу заблокировать себя(((')
            return
        if (await bot.get_chat_member(message.chat.id, user_id_to_ban)).status in ["kicked", "left"]:
            await bot.send_message(message.chat.id, f'Пользователь {message.reply_to_message.from_user.username} уже заблокирован или вышел из чата.')
        else:
            result = await bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id_to_ban)
            if result:
                await bot.send_message(message.chat.id, f'Пользователь {message.reply_to_message.from_user.username} успешно заблокирован!')
            else:
                await bot.send_message(message.chat.id, f'Не получилось(')
    else:
        await bot.send_message(message.chat.id, f'Что-то пошло не так! Чтобы заблокировать пользователя нужно ответить на его сообщение текстом /ban.')

@dp.message_handler(commands=['unban'])
async def unban(message):
    is_not_creator = (await bot.get_chat_member(message.chat.id, message.from_user.id)).status != "creator"
    is_administrator = (await bot.get_chat_member(message.chat.id, message.from_user.id)).status == "administrator"
    if (is_not_creator and not is_administrator) or (is_administrator and (
    await bot.get_chat_member(message.chat.id, message.from_user.id)).can_restrict_members != True):
        await bot.send_message(message.chat.id,
                         f'{message.from_user.username}, у вас нет прав для совершения действия!')
        return
    if message.reply_to_message is not None:
        user_id_to_unban = message.reply_to_message.from_user.id
        if (await bot.get_chat_member(message.chat.id, user_id_to_unban)).status in ["kicked"]:
            result = await bot.unban_chat_member(chat_id=message.chat.id, user_id=user_id_to_unban, only_if_banned=True)
            if result:
                await bot.send_message(message.chat.id,
                                 f'Пользователь {message.reply_to_message.from_user.username} успешно разблокирован!')
            else:
                await bot.send_message(message.chat.id, f'Не получилось(')
        else:
            await bot.send_message(message.chat.id,
                             f'Пользователь {message.reply_to_message.from_user.username} не заблокирован в чате.')
    else:
        await bot.send_message(message.chat.id, f'Что-то пошло не так! Чтобы разблокировать пользователя нужно ответить на его сообщение текстом /unban.')

@dp.message_handler(commands=['promote'])
async def promote(message):
    is_not_creator = (await bot.get_chat_member(message.chat.id, message.from_user.id)).status != "creator"
    is_administrator = (await bot.get_chat_member(message.chat.id, message.from_user.id)).status == "administrator"
    if (is_not_creator and  not is_administrator) or (is_administrator and (await bot.get_chat_member(message.chat.id, message.from_user.id)).can_promote_members != True):
        await bot.send_message(message.chat.id,
                         f'{message.from_user.username}, у вас нет прав для совершения действия!')
        return
    print(message)
    if message.reply_to_message is not None:
        user_id_to_promote = message.reply_to_message.from_user.id
        status = (await bot.get_chat_member(message.chat.id, user_id_to_promote)).status
        if status in ["kicked", "left"]:
            await bot.send_message(message.chat.id, f'Пользователь  {message.reply_to_message.from_user.username} уже заблокирован или вышел из чата.')
        elif status in ["creator", "administrator"]:
            await bot.send_message(message.chat.id, f'Пользователь  {message.reply_to_message.from_user.username} уже является администратором или владельцем группы.')
        else:
            result = await bot.promote_chat_member(chat_id=message.chat.id, user_id=user_id_to_promote,
                                            can_delete_messages=True, can_restrict_members=True,
                                            can_promote_members=True, can_change_info=True, can_invite_users=True,
                                            can_pin_messages=True, can_manage_chat=True, can_manage_video_chats=True)
            if result:
                await bot.send_message(message.chat.id, f'Пользователь {message.reply_to_message.from_user.username} успешно стал администратором!')
            else:
                await bot.send_message(message.chat.id, f'Не получилось(')
    else:
        await bot.send_message(message.chat.id, f'Что-то пошло не так! Чтобы сделать пользователя  администратором нужно ответить на его сообщение текстом /promote.')


@dp.message_handler(commands=['leave'])
async def leave(message):
    await bot.send_message(message.chat.id, f'Пока-пока!')
    await bot.leave_chat(message.chat.id)

@dp.message_handler(commands=['statistics'])
async def statistics(message):
    count = await bot.get_chat_member_count(message.chat.id)
    count_adm = len(await bot.get_chat_administrators(message.chat.id))
    await bot.send_message(message.chat.id, f'Количество участников группы: {count} \n'
                                      f'Количество админов: {count_adm}')
@dp.message_handler(content_types=["new_chat_members"])
async def new_member(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item_1 = types.KeyboardButton("Да!!!!")
    item_2 = types.KeyboardButton("ОЧЕНЬ")
    markup.add(item_1, item_2)
    await bot.send_message(message.chat.id, f'{message.from_user.username}, вы любите папугов?', reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def hide_keybord(message):
    if message.text in ["Да!!!!", "ОЧЕНЬ"] and message.reply_to_message is not None and message.reply_to_message.text == f"{message.from_user.username}, вы любите папугов?":
        await bot.send_message(message.chat.id, text = "Поздравляю, ты прошел проверку!", reply_markup=types.ReplyKeyboardRemove())


executor.start_polling(dp, skip_updates=True)

