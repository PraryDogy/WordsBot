from datetime import datetime
from time import time

import sqlalchemy
from aiogram import types

from database import Dbase, Users
from utilites import (dec_times_append, dec_update_user, update_db_words,
                      users_words, words_find, words_normalize,
                      words_stopwords, words_timer)

def user_update_times(message: types.Message):
    q = (
        sqlalchemy.select(Users.times)
        .filter(Users.user_id==message.from_user.id)
        )
    user_times: str = Dbase.conn.execute(q).first()[0]
    today = datetime.today().replace(microsecond=0)

    if not user_times:
        Dbase.conn.execute(
            sqlalchemy.update(Users)
            .filter(Users.user_id==message.from_user.id)
            .values(
                {"times": str(today) + ','}
                )
            )

    else:
        Dbase.conn.execute(
            sqlalchemy.update(Users)
            .filter(Users.user_id==message.from_user.id)
            .values(
                {"times": f"{user_times},{today},"}
                )
            )

@dec_update_user
# @dec_times_append
async def msg_catch_words(message: types.Message):
    """
    user_id, user_name, chat_id, message
    """
    words = words_find(message.text.split())
    words = words_normalize(words)
    words = list(words_stopwords(words))

    if not users_words.get((message.from_user.id, message.chat.id)):
        users_words[(message.from_user.id, message.chat.id)] = words
    else:
        users_words[(message.from_user.id, message.chat.id)].extend(words)

    if time() - words_timer >= 3600:
        update_db_words()

    # user_update_times(message)