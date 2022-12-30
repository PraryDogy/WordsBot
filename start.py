from aiogram import Bot, Dispatcher, executor, types
import cfg
from utils import write_db, check_user, my_words, chat_words
from PIL import Image
import json

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)
count = 0

@dp.message_handler(commands=['test'])
async def get_awatar(message: types.Message):
    user_id = 536755681
    a = await bot.get_user_profile_photos(user_id=user_id, limit=2)
    
    print(a['photos'])


@dp.message_handler(commands=['my_words'])
async def send_my_words(message: types.Message):
    top = my_words(message.from_user.id, message.chat.id)
    await message.reply(top)


@dp.message_handler(commands=['chat_words'])
async def send_chat_words(message: types.Message):
    top = chat_words(message.chat.id)
    await message.reply(top)


@dp.message_handler()
async def echo(message: types.Message):
    global count
    count += 1
    print(message.text)

    check_user(message.from_user.id, message.from_user.full_name)
    write_db(message.from_user.id, message.chat.id, message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)