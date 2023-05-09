import atexit
from datetime import datetime

from aiogram import executor, types

from bot_config import bot, bot_token, dp
from handlers_msg import (chat_stat, khalisi_msg, msg_catch_words, on_exit,
                          start, temp_stat, user_stat, word_stat, haha)
from inline_msg import create_inline
from webm import download


# dp.register_message_handler(get_file_id,content_types='photo')
dp.register_message_handler(start, commands=['start'])

dp.register_message_handler(download, commands=['video'])


dp.register_message_handler(user_stat, commands=['my_stat'])
dp.register_message_handler(chat_stat, commands=['chat_stat'])

dp.register_message_handler(word_stat, commands=['word_stat'])

dp.register_channel_post_handler(khalisi_msg, regexp='кхалиси')
dp.register_message_handler(khalisi_msg, regexp='кхалиси')

# dp.register_message_handler(
#     temp_stat,
#     content_types=types.ContentType.all()
#     )

dp.register_message_handler(
    msg_catch_words,
    content_types=types.ContentType.all()
    )

dp.register_inline_handler(create_inline)

if __name__ == '__main__':
    atexit.register(on_exit, '')

    inp = input(
            f"Запускаю бота"

            f"\n\n{bot_token[bot._token]}"
            f"\n{bot_token[bot._token]}"
            f"\n{bot_token[bot._token]}"

            "\n\nВвод для отмены, любая буква для старта"
            "\n"
            
        )
    if inp:
        print("\nstart:", datetime.today().replace(microsecond=0))

        try:
            executor.start_polling(
                dp,
                skip_updates=True,
                timeout=800,
                )
        except Exception as e:
            print(e)
