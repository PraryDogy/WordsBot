from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery

import cfg
from bot_config import TOKEN
from database_queries import *
from text_analyser import words_regex
from utils_handler import *
from utils_inline import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['user_words'])
async def send_my_words(message: types.Message):
    db_user_record(message.from_user.id, message.from_user.username)

    msg_del = await bot.send_message(chat_id=message.chat.id, text='Обрабатываю...')

    args = message.get_args()
    msg = user_words_top(message.chat.id, message.from_user.username, args)

    await msg_del.delete()
    await bot.send_message(chat_id=message.chat.id, text=msg)


@dp.message_handler(commands=['chat_words'])
async def send_chat_words(message: types.Message):
    db_user_record(message.from_user.id, message.from_user.username)

    msg_del = await bot.send_message(chat_id=message.chat.id, text='Обрабатываю...')
    top = chat_words_top(message.chat.id, message.from_user.username)
    
    await msg_del.delete()
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


@dp.message_handler(commands=['last_time'])
async def get_msg_t(message: types.Message):
    db_user_record(message.from_user.id, message.from_user.username)
    args = message.get_args()
    await bot.send_message(message.chat.id, text=get_usr_t(message.from_user.username, args))


@dp.message_handler(commands=['gde_svet_denis'])
async def get_ava(message: types.Message):
    db_user_record(message.from_user.id, message.from_user.username)

    user_photos = await bot.get_user_profile_photos(user_id=cfg.feuilletton_id, limit=1)
    last_photo = dict((user_photos.photos[0][-1])).get("file_id")

    file = await bot.get_file(last_photo)
    ava = await bot.download_file(file.file_path, cfg.usr_picture_path)

    if detect_candle(ava.name):
        await bot.send_message(chat_id=message.chat.id, text='Света нет :(')
    else:
        await bot.send_message(chat_id=message.chat.id, text='Свет есть!)')


@dp.inline_handler()
async def inline_libera(inline_query: InlineQuery):
    db_user_record(inline_query.from_user.id, inline_query.from_user.username)

    items = []
    items.append(ItemPuppies(inline_query.from_user.id).item)
    items.append(ItemPenis(inline_query.from_user.id).item)
    items.append(ItemLibera(inline_query.from_user.id).item)
    items.append(ItemFat(inline_query.from_user.id).item)
    items.append(ItemMobi(inline_query.from_user.id).item)

    await bot.answer_inline_query(inline_query.id, results=items, cache_time=1)


@dp.message_handler()
async def echo(message: types.Message):

    if message.via_bot:
        return

    db_user_record(message.from_user.id, message.from_user.username)
    db_time_record(message.from_user.id)
    db_words_record(message.from_user.id, message.chat.id, words_regex(message.text))


if __name__ == '__main__':
    inp = input(
        'Вы уверены, что сменили токен бота? Напишите любую букву и нажми ввод. Для отмены нажмите только ввод\n')
    if inp:
        Dbase.base.metadata.create_all(Dbase.conn)
        executor.start_polling(dp, skip_updates=True)
