from datetime import datetime, timedelta

from aiogram import executor, types
from aiogram.types import InlineQuery

from bot_config import bot, dp
from handlers_msg import (chat_words_top, khalisi_msg, msg_catch_words, start,
                          top_boltunov, user_words_top, word_stat)
from inline_msg import inline_tests

# dp.register_message_handler(get_file_id,content_types='photo')
dp.register_message_handler(start, commands=['start'])

dp.register_message_handler(user_words_top, commands=['user_words'])
dp.register_message_handler(chat_words_top, commands=['chat_words'])
dp.register_message_handler(top_boltunov, commands=['top_boltunov'])
dp.register_message_handler(word_stat, commands=['word_stat'])

dp.register_channel_post_handler(khalisi_msg, regexp='кхалиси')
dp.register_message_handler(khalisi_msg, regexp='кхалиси')

dp.register_message_handler(msg_catch_words)

dp.register_inline_handler(inline_tests)


if __name__ == '__main__':
    inp = input(
        'Вы уверены, что сменили токен бота? Напишите любую букву и нажми ввод. Для отмены нажмите только ввод\n')
    if inp:
        executor.start_polling(dp, skip_updates=True, timeout=20)
