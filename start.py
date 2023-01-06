import re

import clipboard
from aiogram import executor, types
from aiogram.types import InlineQuery

import cfg
from bot_config import bot, dp
from handler_utils import (chat_words, detect_candle, get_usr_t,
                               top_boltunov, user_words_top)
from inline_utils import ItemFat, ItemLibera, ItemPuppy
from utils import db_user_check, db_words_record, words_convert, db_time_record


@dp.message_handler(commands=['user_words'])
async def send_my_words(message: types.Message):
    db_user_check(message.from_user.id, message.from_user.username)
    
    usr_name = message.get_args().replace('@', '')
    usr_name = message.from_user.username if not usr_name else usr_name

    top = user_words_top(message.chat.id, usr_name)
    await bot.send_message(chat_id=message.chat.id, text=top)


@dp.message_handler(commands=['chat_words'])
async def send_chat_words(message: types.Message):
    db_user_check(message.from_user.id, message.from_user.username)
    top = chat_words(message.chat.id, message.from_user.username)
    await bot.send_message(chat_id=message.chat.id, text=top)


@dp.message_handler(commands=['top_boltunov'])
async def top_slovobludov(message: types.Message):
    db_user_check(message.from_user.id, message.from_user.username)
    msg = top_boltunov(message.chat.id, message.from_user.username)
    await bot.send_message(chat_id=message.chat.id, text=msg)


@dp.message_handler(commands=['last_time'])
async def get_msg_t(message: types.Message):
    db_user_check(message.from_user.id, message.from_user.username)
    nickname = message.get_args().replace('@', '')
    await bot.send_message(message.chat.id, text=get_usr_t(message.from_user.username, nickname))


@dp.message_handler(commands=['gde_svet_denis'])
async def get_ava(message: types.Message):
    db_user_check(message.from_user.id, message.from_user.username)

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
    db_user_check(inline_query.from_user.id, inline_query.from_user.username)
    item_libera = ItemLibera(inline_query.from_user.id).item
    item_fat = ItemFat(inline_query.from_user.id).item
    item_puppy = ItemPuppy(inline_query.from_user.id).item

    items = [item_libera, item_fat, item_puppy]
    await bot.answer_inline_query(inline_query.id, results=items, cache_time=1)


# @dp.message_handler(content_types=['animation'])
# async def get_sticker_id(message):
#     reg = r'"file_id": "\S*"'
#     res = re.findall(reg, str(message))
#     file_id = res[-1].split(' ')[-1].strip('"')
#     clipboard.copy(file_id)
#     print(file_id)


@dp.message_handler()
async def echo(message: types.Message):
    if message.via_bot:
        return
    db_user_check(message.from_user.id, message.from_user.username)
    db_time_record(message.from_user.id)
    db_words_record(message.from_user.id, message.chat.id, words_convert(message.text))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)