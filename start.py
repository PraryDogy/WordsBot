from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery

from bot_config import TOKEN
from handlers import (msg_catch_words, chat_words_top, top_boltunov,
                      user_words_top, word_stat)
from inline_tests import (ItemAss, ItemDestiny, ItemEat, ItemFat, ItemLibera,
                          ItemMobi, ItemPenis, ItemPokemons, ItemPuppies,
                          ItemZarplata)
from start_utils import khalisi, user_data, user_update_time, user_update_times

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['user_words'])
async def send_my_words(message: types.Message):
    user = user_data(message.from_user.id, message.from_user.username)
    msg = user_words_top(message.chat.id, user, 500)
    await bot.send_message(chat_id=message.chat.id, text=msg)


@dp.message_handler(commands=['chat_words'])
async def send_chat_words(message: types.Message):
    user = user_data(message.from_user.id, message.from_user.username)
    top = chat_words_top(message.chat.id, user, 500)
    await bot.send_message(chat_id=message.chat.id, text=top)


@dp.message_handler(commands=['top_boltunov'])
async def top_slovobludov(message: types.Message):
    user = user_data(message.from_user.id, message.from_user.username)
    msg = top_boltunov(message.chat.id, user)
    await bot.send_message(chat_id=message.chat.id, text=msg)


@dp.message_handler(commands=['word_stat'])
async def get_word_stat(message: types.Message):
    user_data(message.from_user.id, message.from_user.username)
    args = message.get_args()
    await bot.send_message(
        message.chat.id, text=word_stat(message.chat.id, args))

# from test import gpt

# @dp.message_handler(commands=['destiny'])
# async def start(message: types.Message):
#     # bot = ChatGPT()
#     # response = bot.ask("Когда появился человек?")

#     await gpt()

#     await bot.send_message(chat_id=message.chat.id, text='')


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
    user = user_data(inline_query.from_user.id, inline_query.from_user.username)
    today = datetime.today()
    need_update = bool((today - user['user_time']) > timedelta(hours=3))

    if need_update:
        user_update_time(user['user_id'], today)

    items = []
    for test in (
        ItemDestiny, ItemPokemons, ItemPuppies, ItemEat, ItemFat, ItemPenis, 
        ItemAss, ItemZarplata, ItemLibera, ItemMobi, ):
        items.append(
            test(
                user['user_id'], user['user_time'], today, need_update,
                inline_query.query).item)

    await bot.answer_inline_query(
        inline_query.id, results=items, is_personal=True, cache_time=0)


@dp.message_handler()
async def echo(message: types.Message):

    if message.via_bot:
        return

    await khalisi(message, bot)

    user_data(message.from_user.id, message.from_user.username)
    user_update_times(message.from_user.id)
    msg_catch_words(message.from_user.id, message.chat.id, message.text)


if __name__ == '__main__':
    inp = input(
        'Вы уверены, что сменили токен бота? Напишите любую букву и нажми ввод. Для отмены нажмите только ввод\n')
    if inp:
        executor.start_polling(dp, skip_updates=True, timeout=20)
