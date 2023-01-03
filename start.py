from aiogram import Bot, Dispatcher, executor, types, utils
import cfg
from utils import write_db, check_user, my_words, chat_words, den_light, libera_func
from asyncio import sleep


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
            print(last_photo)
            counter += 1

    if counter == 5:
        return

    ava = await bot.download_file(file.file_path, 'ava.png')
    if den_light(ava.name):
        await bot.send_message(chat_id=message.chat.id, text='Света нет :(')
    else:
        await bot.send_message(chat_id=message.chat.id, text='Свет есть!)')


@dp.message_handler()
async def echo(message: types.Message):
    check_user(message.from_user.id, message.from_user.full_name)
    write_db(message.from_user.id, message.chat.id, message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)