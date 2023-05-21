from pick import pick
from bot_token import TOKEN_DICT


title = 'Выберите бота:'
options = [i for i in TOKEN_DICT]

option, index = pick(options, title, indicator='=>', default_index=0)

print(option, index)