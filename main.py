from aiogram import executor

from all_handlers.message import start
from bot_config import dp

dp.register_message_handler(start, commands=['start', 'info'])


if __name__ == '__main__':
    inp = input(
        'Вы уверены, что сменили токен бота? Напишите любую букву и нажми ввод. Для отмены нажмите только ввод\n')
    if inp:
        executor.start_polling(dp, skip_updates=True, timeout=20)