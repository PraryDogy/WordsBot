from aiogram import executor

from all_handlers.message import info, user_words_top
from bot_config import dp

dp.register_message_handler(info, commands=['start', 'info'])
dp.register_message_handler(user_words_top, commands=['user_words'])


if __name__ == '__main__':
    inp = input(
        "Вы уверены, что сменили токен бота?"
        "Напишите любую букву и нажмите ввод. Для отмены нажмите только ввод\n"
        )
    if inp:
        executor.start_polling(dp, skip_updates=True, timeout=20)