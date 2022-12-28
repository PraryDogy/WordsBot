from aiogram import Bot, Dispatcher, executor, types
import cfg
from database import Dbase, Words
from utils import get_words, check_user


bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)
words = []


@dp.message_handler()
async def echo(message: types.Message):
    info = (message.from_user.id, message.from_user.full_name, get_words(message.text))

    check_user(message.from_user.id, message.from_user.full_name)





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)