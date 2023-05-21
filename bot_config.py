from aiogram import Bot, Dispatcher
from pick import pick

from bot_token import TOKEN_DICT

# multiple bots
# TOKEN_DICT = {"bot name any": "token"}

title = 'Выберите бота'

title = 'Выберите бота:'
options = [i for i in TOKEN_DICT]
bot_name, index = pick(options, title, indicator='=>', default_index=0)

print(f"Выбран {bot_name}")
token = TOKEN_DICT[bot_name]

bot = Bot(token)
dp = Dispatcher(bot)

BOT_NAME = "prariewords_bot"
SQL_LIMIT = 300


evlosh = 248208655
evlosh_name = 'evlosh'

peugeot = 5717544572
peugeot_name = 'PeugeotKiller'

heli = -1001297579871
new_trup = -1001891371765

