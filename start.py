from asyncio import sleep

from aiogram import Bot, Dispatcher, executor, types, utils
from aiogram.types.input_file import InputFile

import cfg
from utils import *

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['my_words'])
async def send_my_words(message: types.Message):
    top = my_words(message.from_user.id, message.chat.id, message.from_user.username)
    await bot.send_message(chat_id=message.chat.id, text=top)


@dp.message_handler(commands=['chat_words'])
async def send_chat_words(message: types.Message):
    top = chat_words(message.chat.id, message.from_user.username)
    await bot.send_message(chat_id=message.chat.id, text=top)


@dp.message_handler(commands=['libera_test'])
async def libera_test(message: types.Message):
    msg = libera_func(message.from_user.id, message.from_user.username)
    await bot.send_message(chat_id=message.chat.id, text=msg)


@dp.message_handler(commands=['top_boltunov'])
async def top_slovobludov(message: types.Message):
    msg = top_boltunov(message.chat.id, message.from_user.username)
    await bot.send_message(chat_id=message.chat.id, text=msg)


@dp.message_handler(commands=['gde_svet_denis'])
async def get_ava(message: types.Message):
    feu = 536755681
    counter = 0
    while counter < 5:

        try:
            user_photos = await bot.get_user_profile_photos(user_id=feu, limit=1)
            last_photo = dict((user_photos.photos[0][-1])).get("file_id")
            file = await bot.get_file(last_photo)
            counter = 6

        except utils.exceptions.BadRequest:
            await sleep(1)
            user_photos = await bot.get_user_profile_photos(user_id=feu, limit=1)
            last_photo = dict((user_photos.photos[0][-1])).get("file_id")
            counter += 1

    if counter == 5:
        return

    ava = await bot.download_file(file.file_path, './img/ava.png')
    if den_light(ava.name):
        await bot.send_message(chat_id=message.chat.id, text='Света нет :(')
    else:
        await bot.send_message(chat_id=message.chat.id, text='Свет есть!)')


@dp.message_handler()
async def echo(message: types.Message):
    check_user(message.from_user.id, message.from_user.username)
    words_list = words_convert(message.text)

    pres = president(words_list)
    if pres:
        stick = InputFile(pres)
        await bot.send_sticker(
            message.chat.id,
            sticker=stick,
            reply_to_message_id=message.message_id
            )

    write_db(message.from_user.id, message.chat.id, words_list)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)