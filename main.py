from aiogram import Bot, Dispatcher, executor, types
import cfg
from database import Dbase, Words
from utils import write_db, check_user


bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    print('message catched')
    check_user(message.from_user.id, message.from_user.full_name)
    write_db(message.from_user.id, message.from_user.full_name, message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)