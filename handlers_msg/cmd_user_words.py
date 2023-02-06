import sqlalchemy
from aiogram import types

from bot_config import bot
from database import Dbase, Words
from utilites import dec_words_update, dec_update_user, get_nouns


def user_words_get(usr_id, msg_chat_id, limit: int):
    """
    Returns dict (word: count) for current user and chat, ordered by count.
    * `words_limit`: optional, `int`.
    """
    q = sqlalchemy.select(Words.word, Words.count)\
        .where(Words.user_id==usr_id, Words.chat_id==msg_chat_id)\
        .order_by(-Words.count).limit(limit)
    return dict(Dbase.conn.execute(q).all())


def create_msg(message: types.Message, limit: int):
    """
    user_id, user_name, chat_id, limit
    limit: how many words load from database to create top words,
    500 recomended.
    """

    words = user_words_get(
        message.from_user.id, message.chat.id, limit)

    nouns = {
        nn: words[nn]
        for nn in get_nouns(words.keys())
        }

    msg = (
        f"@{message.from_user.username}, ваш топ 10 слов:",
        *[
            f"{x}: {y}"
            for x, y in tuple(words.items())[:10]
            ],
        '\nТоп 10 существительных:',
        *[
            f'{x}: {y}'
            for x, y in tuple(nouns.items())[:10]
            ],
            )

    return '\n'.join(msg)


@dec_update_user
@dec_words_update
async def send_msg(message: types.Message):
    msg = create_msg(message, limit=500)
    await bot.send_message(chat_id=message.chat.id, text=msg)