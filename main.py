from aiogram import Bot, Dispatcher, executor, types
import cfg
from database import Dbase, Words
from utils import write_db, check_user, users_list


bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)
data = []


@dp.message_handler()
async def echo(message: types.Message):
    # check_user(message.from_user.id, message.from_user.full_name)
    val = 0
    info = (message.from_user.id, message.from_user.full_name, message.text)
    data.append(info)

    if len(data) > val:
        for id, name in users_list(data):
            check_user(id, name)

        for id, name, words in data:
            write_db(id, name, words)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)