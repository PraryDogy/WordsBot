from aiogram import Bot, Dispatcher, executor, types
import cfg
from utils import write_db, check_user, my_words, chat_words, den_light


bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)
count = 0



@dp.message_handler(commands=['test'])
async def get_ava(message: types.Message):
    feu = 536755681

    user_photos = await bot.get_user_profile_photos(user_id=feu, limit=2)
    if len(user_photos.photos[0]) == 0:
        return

    last_photo = dict((user_photos.photos[0][-1])).get("file_id")
    file = await bot.get_file(last_photo)
    ava = await bot.download_file(file.file_path, 'ava.png')


@dp.message_handler(commands=['my_words'])
async def send_my_words(message: types.Message):
    # await message.reply('фигушки')
    # return
    top = my_words(message.from_user.id, message.chat.id)
    await message.reply(top)


@dp.message_handler(commands=['chat_words'])
async def send_chat_words(message: types.Message):
    # await message.reply('фигушки')
    # return
    top = chat_words(message.chat.id)
    await message.reply(top)


@dp.message_handler(commands=['gde_svet_denis'])
async def get_ava(message: types.Message):
    feu = 536755681

    user_photos = await bot.get_user_profile_photos(user_id=feu, limit=2)
    if len(user_photos.photos[0]) == 0:
        return

    last_photo = dict((user_photos.photos[-1][0])).get("file_id")
    file = await bot.get_file(last_photo)
    ava = await bot.download_file(file.file_path, 'ava.png')

    if den_light(ava.name):
        await bot.send_message(chat_id=message.chat.id, text='Света нет :(')
    else:
        await bot.send_message(chat_id=message.chat.id, text='Свет есть!)')


@dp.message_handler()
async def echo(message: types.Message):
    global count
    count += 1

    check_user(message.from_user.id, message.from_user.full_name)
    write_db(message.from_user.id, message.chat.id, message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)