from collections import Counter
from datetime import datetime

import sqlalchemy

from database import Dbase, Users, Words


def db_user_record(msg_user_id: int, msg_username: str):
    """
    Checks database `Users` table for user by `user_id` from message.
    Creates new record if user not exists.
    Updates username of exists user if it was changed.
    """
    get_user = sqlalchemy.select(
        Users.user_id, Users.user_name).filter(Users.user_id == msg_user_id)
    db_user = Dbase.conn.execute(get_user).first()

    if not db_user:
        vals = {'user_id': msg_user_id, 'user_name': msg_username}
        new_user = sqlalchemy.insert(Users).values(vals)
        Dbase.conn.execute(new_user)

    elif msg_username != db_user[1]:
        vals = {'user_name': msg_username}
        update_user = sqlalchemy.update(Users)\
            .where(Users.user_id==msg_user_id).values(vals)
        Dbase.conn.execute(update_user)



def db_words_record(msg_usr_id, msg_chat_id, words_list):
    """
    Gets all user's words with all chats ids  from database
    If word from input words list not in database words list - adds new row
    If word in database words list but has other chat id - adds new row
    If word in database words list and has the same chat id - updates word counter
    * `words_list`: list of words
    """
    for i in words_list:
        query = sqlalchemy.select(Words.id, Words.word, Words.count)\
            .where(Words.user_id==msg_usr_id, Words.chat_id==msg_chat_id)
        db_data = Dbase.conn.execute(query).all()

    db_words = [i[1] for i in db_data]
    new_words = Counter([i for i in words_list if i not in db_words])

    for w, c in new_words.items():
        vals = {'word': w, 'count': c, 'user_id': msg_usr_id, 'chat_id': msg_chat_id}
        q = sqlalchemy.insert(Words).values(vals)
        Dbase.conn.execute(q)

    old_words = [(x, y, z) for x, y, z in db_data if y in words_list]

    for x, y, z in old_words:
        vals = {'count': z + len([i for i in words_list if i == y])}
        q = sqlalchemy.update(Words).where(Words.id==x).values(vals)
        Dbase.conn.execute(q)


def db_time_record(msg_usr_id):
    """
    Record when user send message last time.
    """
    vals = {'last_time': datetime.today().replace(microsecond=0)}
    q = sqlalchemy.update(Users).where(Users.user_id==msg_usr_id).values(vals)
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


def db_user_time_get(username):
    """
    Returns db datetime `str` or `None`
    """
    q = sqlalchemy.select(Users.last_time).where(Users.user_name==username)
    return Dbase.conn.execute(q).first()


def db_user_words_get(usr_id, msg_chat_id, words_limit=None):
    """
    Returns tuple tuples (`word`, `count`) for current user and chat, ordered by count.
    * `words_limit`: optional, `int`.
    """
    q = sqlalchemy.select(Words.word, Words.count)\
        .where(Words.user_id==usr_id, Words.chat_id==msg_chat_id)\
        .order_by(-Words.count).limit(words_limit)
    return Dbase.conn.execute(q).all()


def db_word_stat_get(msg_chat_id, args):
    """
    Returns `tuple` (how many people saif word, how many times people said word)
    or None if word not found
    """
    q = sqlalchemy.select(
        Dbase.sq_count(Words.word),\
        Dbase.sq_sum(Words.count))\
        .filter(Words.chat_id==msg_chat_id, Words.word==args)
    return Dbase.conn.execute(q).first()


def db_word_stat_get(msg_chat_id, input_word):
    """
    Returns `list`:
    * `set` similar words including `input_word`,
    * `int` total how many times people said input word & similar words
    * `int` total how many people said input & similar words

    Returns `False` if `input_word` and similar words not in database.
    """
    res = []

    q = sqlalchemy.select(Words.word)\
        .filter(Words.chat_id==msg_chat_id, Words.word.like('%'+input_word+'%'))
    res.append(set(i[0] for i in Dbase.conn.execute(q).all()))

    q = sqlalchemy.select(Dbase.sq_sum(Words.count))\
        .filter(Words.chat_id==msg_chat_id, Words.word.in_(res[0]))
    res.append(Dbase.conn.execute(q).first()[0])

    q = sqlalchemy.select(Dbase.sq_count(Words.word))\
        .filter(Words.chat_id==msg_chat_id, Words.word.in_(res[0]))
    res.append(Dbase.conn.execute(q).first()[0])

    return False if not res[0] else res
