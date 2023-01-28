from collections import Counter
from datetime import datetime, timedelta

import sqlalchemy

from database import *


def db_all_usernames_get():
    """
    Returns tuple (user_id, user_name) for all users.
    """
    q = sqlalchemy.select(Users.user_id, Users.user_name)
    return Dbase.conn.execute(q).all()


def chat_words_get(chat_id: int, limit: int):
    q = (
        sqlalchemy.select(Words.word, Words.count)
        .filter(Words.chat_id==chat_id)
        .order_by(-Words.count)
        .limit(limit)
        )
    return Dbase.conn.execute(q).fetchall()


def user_get_words(usr_id, msg_chat_id, words_limit: int):
    """
    Returns dict (word: count) for current user and chat, ordered by count.
    * `words_limit`: optional, `int`.
    """
    q = sqlalchemy.select(Words.word, Words.count)\
        .where(Words.user_id==usr_id, Words.chat_id==msg_chat_id)\
        .order_by(-Words.count).limit(words_limit)
    return dict(Dbase.conn.execute(q).all())


def db_sim_words(msg_chat_id, input_word):
    q = sqlalchemy.select(Words.word)\
    .filter(Words.chat_id==msg_chat_id, Words.word.like('%'+input_word+'%'))
    return set(i[0] for i in Dbase.conn.execute(q).all())


def db_word_count(msg_chat_id, words_list):
    q = sqlalchemy.select(Dbase.sq_sum(Words.count))\
        .filter(Words.chat_id==msg_chat_id, Words.word.in_(words_list))
    return Dbase.conn.execute(q).first()[0]


def db_word_people(msg_chat_id, words_list):
    q = sqlalchemy.select(Words.user_id)\
        .filter(Words.chat_id==msg_chat_id, Words.word.in_(words_list))

    return set(i[0] for i in Dbase.conn.execute(q).all())