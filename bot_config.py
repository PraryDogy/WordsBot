from aiogram import Bot, Dispatcher
from pick import pick

from bot_token import TOKEN_DICT

# multiple bots
# TOKEN_DICT = {"bot name any": "token"}

title = 'Выберите бота:'
options = [i for i in TOKEN_DICT]
bot_name, index = pick(options, title, indicator='=>', default_index=0)

print(f"Выбран {bot_name}")

token = TOKEN_DICT[bot_name]

bot = Bot(token)
dp = Dispatcher(bot)

SQL_LIMIT = 300
