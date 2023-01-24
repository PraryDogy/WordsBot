from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import *

from bot_config import TOKEN
from handler_commands import *
from inline_tests import *
from start_utils import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['user_words'])
async def send_my_words(message: types.Message):
    db_user_record(message.from_user.id, message.from_user.username)
    args = message.get_args()
    msg = user_words_top(message.chat.id, message.from_user.username, args)
    await bot.send_message(chat_id=message.chat.id, text=msg)


@dp.message_handler(commands=['chat_words'])
async def send_chat_words(message: types.Message):
    db_user_record(message.from_user.id, message.from_user.username)
    top = chat_words_top(message.chat.id, message.from_user.username)
    await bot.send_message(chat_id=message.chat.id, text=top)


@dp.message_handler(commands=['top_boltunov'])
async def top_slovobludov(message: types.Message):
    db_user_record(message.from_user.id, message.from_user.username)
    msg = top_boltunov(message.chat.id, message.from_user.username)
    await bot.send_message(chat_id=message.chat.id, text=msg)


@dp.message_handler(commands=['word_stat'])
async def get_word_stat(message: types.Message):
    db_user_record(message.from_user.id, message.from_user.username)
    args = message.get_args()
    await bot.send_message(message.chat.id, text=word_stat(message.chat.id, args))


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    with open('txt_start.txt', 'r') as file:
        data = file.read()
    await bot.send_message(chat_id=message.chat.id, text=data)


# @dp.message_handler(content_types='photo')
# async def get_word_stat(message: types.Message):
#     try:
#         print(get_file_id(message))
#     except Exception:
#         print('no file id')


@dp.inline_handler()
async def inline_libera(inline_query: InlineQuery):
    db_user_record(inline_query.from_user.id, inline_query.from_user.username)

    user_time, today, need_update = prepare_test(inline_query.from_user.id)
    update_user_time(need_update, today, inline_query.from_user.id)

    items = []
    for test in (ItemDestiny, ItemPokemons, ItemPuppies, ItemFat, ItemVgg,\
    ItemPenis, ItemAss, ItemZarplata, ItemLibera, ItemMobi):
        items.append(
            test(
                inline_query.from_user.id,
                user_time, today, need_update,
                inline_query.query).item)

    await bot.answer_inline_query(inline_query.id, results=items, is_personal=True)


@dp.message_handler()
async def echo(message: types.Message):

    if message.via_bot:
        return

    # dp.loop.create_task(khalisi(message, bot))
    await khalisi(message, bot)

    db_user_record(message.from_user.id, message.from_user.username)
    users_words(message.from_user.id, message.chat.id, message.text)


if __name__ == '__main__':
    inp = input(
        'Вы уверены, что сменили токен бота? Напишите любую букву и нажми ввод. Для отмены нажмите только ввод\n')
    if inp:
        Dbase.base.metadata.create_all(Dbase.conn)
        executor.start_polling(dp, skip_updates=True, timeout=20)
