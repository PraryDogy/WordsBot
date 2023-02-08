import atexit
from datetime import datetime

from aiogram import executor

from bot_config import dp
from handlers_msg import (chat_words_top, khalisi_msg, msg_catch_words,
                          my_stat, on_exit, start, top_boltunov,
                          user_words_top, word_stat)
from inline_msg import create_inline

# dp.register_message_handler(get_file_id,content_types='photo')
dp.register_message_handler(start, commands=['start'])


dp.register_message_handler(my_stat, commands=['my_stat'])
dp.register_message_handler(user_words_top, commands=['my_words'])
dp.register_message_handler(chat_words_top, commands=['chat_words'])
dp.register_message_handler(top_boltunov, commands=['top_boltunov'])
dp.register_message_handler(word_stat, commands=['word_stat'])

dp.register_channel_post_handler(khalisi_msg, regexp='кхалиси')
dp.register_message_handler(khalisi_msg, regexp='кхалиси')

dp.register_message_handler(msg_catch_words)

dp.register_inline_handler(create_inline)


if __name__ == '__main__':
    atexit.register(on_exit, '')

    inp = input(
            "Вы уверены, что сменили токен бота? Напишите любую букву и "
            "нажмите ввод. Для отмены нажмите только ввод.\n"
        )
    if inp:
        print("\nstart:", datetime.today().replace(microsecond=0))
        executor.start_polling(dp, skip_updates=True, timeout=20)

