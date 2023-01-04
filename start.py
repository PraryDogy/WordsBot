from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery
from aiogram.types.input_file import InputFile

import cfg
from inline_utils import ItemFat, ItemLibera
from utils import (chat_words, check_user, detect_candle, my_words,
                   president_word, top_boltunov, words_convert, write_db)

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['my_words'])
async def send_my_words(message: types.Message):
    check_user(message.from_user.id, message.from_user.username)
    top = my_words(message.from_user.id, message.chat.id, message.from_user.username)
    await bot.send_message(chat_id=message.chat.id, text=top)


@dp.message_handler(commands=['chat_words'])
async def send_chat_words(message: types.Message):
    check_user(message.from_user.id, message.from_user.username)
    top = chat_words(message.chat.id, message.from_user.username)
    await bot.send_message(chat_id=message.chat.id, text=top)


@dp.message_handler(commands=['top_boltunov'])
async def top_slovobludov(message: types.Message):
    check_user(message.from_user.id, message.from_user.username)
    msg = top_boltunov(message.chat.id, message.from_user.username)
    await bot.send_message(chat_id=message.chat.id, text=msg)


@dp.message_handler(commands=['gde_svet_denis'])
async def get_ava(message: types.Message):
    check_user(message.from_user.id, message.from_user.username)

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
    check_user(inline_query.from_user.id, inline_query.from_user.username)
    item_libera = ItemLibera(inline_query.from_user.id).item
    item_fat = ItemFat(inline_query.from_user.id).item

    items = [item_libera, item_fat]
    await bot.answer_inline_query(inline_query.id, results=items, cache_time=1)


@dp.message_handler()
async def echo(message: types.Message):
    if message.via_bot:
        return

    check_user(message.from_user.id, message.from_user.username)
    words_list = words_convert(message.text)

    pres = president_word(words_list)
    if pres:
        stick = InputFile(pres)
        await bot.send_sticker(
            message.chat.id, sticker=stick, reply_to_message_id=message.message_id)

    write_db(message.from_user.id, message.chat.id, words_list)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)