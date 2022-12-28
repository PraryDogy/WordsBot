from aiogram import Bot, Dispatcher, executor, types
import cfg
from database import Dbase, Words
from utils import get_words, check_user


bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)
data = []


@dp.message_handler()
async def echo(message: types.Message):
    # check_user(message.from_user.id, message.from_user.full_name)
    val = 1
    info = (message.from_user.id, message.from_user.full_name, get_words(message.text))
    data.append(info)

    if len(data) > val:
        
        user_ids = set((i[0], i[1]) for i in data)
        for id, name in user_ids:
            print('check_user')
            check_user(id, name)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)