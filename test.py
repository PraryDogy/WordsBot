import random
import time
from datetime import datetime
from datetime import time as dtime

import sqlalchemy

from database import Dbase, Libera, Words, Users
from dicts import libera, no_libera
from utils import words_convert

def top_boltunov(msg_chat_id, msg_username):
    q = sqlalchemy.select(Users.user_id, Users.user_name)
    db_users = Dbase.conn.execute(q).fetchall()

    user_words = []

    for db_id, db_user_name in db_users:
        q = sqlalchemy.select(Words.count).where(Words.chat_id==msg_chat_id, Words.user_id==db_id)
        words_count = sum(i[0] for i in Dbase.conn.execute(q).fetchall())
        user_words.append((db_user_name, words_count))

    user_words = sorted(user_words, key=lambda x: x[1])
    user_words.reverse()
    user_words = user_words[:10]
    user_words = '\n'.join(f'{i[0]}: {i[1]} слов' for i in user_words)
    return (
        f'@{msg_username}, топ словоблудов:\n\n'
        f'{user_words}'
        )

# print(top_boltunov(-1001297579871, 'evlosh', ))
