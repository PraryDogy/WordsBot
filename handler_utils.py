from collections import Counter
from datetime import datetime, timedelta

import sqlalchemy

from database import *


def db_words_record(user: tuple, word_list: list):
    if not word_list:
        return

    user_id, chat_id = user

    q = (
        sqlalchemy.select(Words.word, Words.count).
        filter(Words.user_id==user_id, Words.chat_id==chat_id, Words.word.in_(word_list))
        )

    db_words = dict(Dbase.conn.execute(q).all())
    msg_words = dict(Counter(word_list))
    old_words = {k: db_words[k] + msg_words[k] for k in (db_words)}

    q = (
        sqlalchemy.update(Words)
        .filter(Words.word.in_(old_words), Words.user_id==user_id, Words.chat_id==chat_id)
        .values({Words.count: sqlalchemy.case(old_words, value=Words.word)})
        )

    if old_words:
        Dbase.conn.execute(q)

    new_words = dict(Counter([i for i in word_list if i not in old_words]))

    values = [{
        'word': x, 'count': y, 'user_id': user_id, 'chat_id': chat_id
        } for x, y in new_words.items()]
    q = sqlalchemy.insert(Words).values(values)

    if values:
        Dbase.conn.execute(q)


def db_user_get(username: str):
    """
    Returns `user_id`, `username` or None
    """
    q = sqlalchemy.select(Users.user_id, Users.user_name)\
        .filter(Dbase.sq_lower(Users.user_name)==username.lower())
    return Dbase.conn.execute(q).first()


def db_all_usernames_get():
    """
    Returns tuple (user_id, user_name) for all users.
    """
    q = sqlalchemy.select(Users.user_id, Users.user_name)
    return Dbase.conn.execute(q).all()


def db_chat_words_get(msg_chat_id, words_limit=None):
    """
    Returns tuple tuples (`word`, `count`) for chat.
    * `words_limit`: optional, `int`.
    """
    q = sqlalchemy.select(Words.word, Words.count)\
        .where(Words.chat_id==msg_chat_id).order_by(-Words.count)\
        .limit(words_limit)
    return Dbase.conn.execute(q).fetchall()


def db_user_words_get(usr_id, msg_chat_id, words_limit=None):
    """
    Returns tuple tuples (`word`, `count`) for current user and chat, ordered by count.
    * `words_limit`: optional, `int`.
    """
    q = sqlalchemy.select(Words.word, Words.count)\
        .where(Words.user_id==usr_id, Words.chat_id==msg_chat_id)\
        .order_by(-Words.count).limit(words_limit)
    return Dbase.conn.execute(q).all()


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