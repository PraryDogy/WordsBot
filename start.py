from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery

from bot_config import dp, bot
from handlers import (msg_catch_words, chat_words_top, top_boltunov,
                      user_words_top, word_stat)
from inline_tests import (ItemAss, ItemDestiny, ItemEat, ItemFat, ItemLibera,
                          ItemMobi, ItemPenis, ItemPokemons, ItemPuppies,
                          ItemZarplata)
from start_utils import khalisi, user_data, user_update_time, user_update_times


@dp.message_handler(commands=['user_words'])
async def send_my_words(message: types.Message):
    msg = user_words_top(
        user_id = message.from_user.id,
        user_name = message.from_user.username,
        chat_id = message.chat.id,
        limit=500
        )
    await bot.send_message(chat_id=message.chat.id, text=msg)


@dp.message_handler(commands=['chat_words'])
async def send_chat_words(message: types.Message):
    msg = chat_words_top(
        user_id = message.from_user.id,
        user_name = message.from_user.username,
        chat_id = message.chat.id,
        limit=500
        )
    await bot.send_message(chat_id=message.chat.id, text=msg)


@dp.message_handler(commands=['top_boltunov'])
async def top_slovobludov(message: types.Message):
    msg = top_boltunov(
        user_id = message.from_user.id,
        user_name = message.from_user.username,
        chat_id = message.chat.id,
        )
    await bot.send_message(chat_id=message.chat.id, text=msg)


@dp.message_handler(commands=['word_stat'])
async def get_word_stat(message: types.Message):

    msg = word_stat(
        word = message.get_args(),
        user_id = message.from_user.id,
        user_name = message.from_user.username,
        chat_id = message.chat.id,
        )
    await bot.send_message(message.chat.id, text=msg)


# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     with open('txt_start.txt', 'r') as file:
#         data = file.read()
#     await bot.send_message(chat_id=message.chat.id, text=data)


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


@dp.channel_post_handler(content_types='text')
async def channel_khalisi(message: types.Message):
    await khalisi(message, bot)


@dp.message_handler()
async def echo(message: types.Message):

    if message.via_bot:
        return

    await khalisi(message, bot)

    # user_update_times(message.from_user.id)

    msg_catch_words(
        user_id = message.from_user.id,
        user_name = message.from_user.username,
        chat_id = message.chat.id,
        message = message.text
        )


if __name__ == '__main__':
    inp = input(
        'Вы уверены, что сменили токен бота? Напишите любую букву и нажми ввод. Для отмены нажмите только ввод\n')
    if inp:
        executor.start_polling(dp, skip_updates=True, timeout=20)
