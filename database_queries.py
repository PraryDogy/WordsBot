from datetime import datetime

import sqlalchemy

from database import Dbase, Users, Words


def db_user_check(msg_user_id: int, msg_username: str):
    """
    Checks database `Users` table for user by `user_id` from message.
    Creates new record if user not exists.
    Updates username of exists user if it was changed.
    """
    get_user = sqlalchemy.select(
        Users.user_id, Users.user_name).filter(Users.user_id == msg_user_id)
    db_user = Dbase.conn.execute(get_user).first()
    
    if db_user is not None:
        db_id, db_name = db_user
        if msg_username != db_name:
            vals = {'user_name': msg_username}
            update_user = sqlalchemy.update(Users).where(Users.user_id==msg_user_id).values(vals)
            Dbase.conn.execute(update_user)

    if db_user is None:
        vals = {'user_id': msg_user_id, 'user_name': msg_username}
        new_user = sqlalchemy.insert(Users).values(vals)
        Dbase.conn.execute(new_user)



def db_words_record(msg_user_id, msg_chat_id, words_list):
    """
    Gets all user's words with all chats ids  from database
    If word from input words list not in database words list - adds new row
    If word in database words list but has other chat id - adds new row
    If word in database words list and has the same chat id - updates word counter
    * `words_list`: list of words
    """
    query = sqlalchemy.select(Words.word, Words.chat_id).where(Words.user_id==msg_user_id)
    db_user_words = list(Dbase.conn.execute(query).fetchall())
    new_words = []

    for word in words_list:
        if (word, msg_chat_id) not in db_user_words and \
            (word, msg_chat_id) not in new_words:

            new_words.append((word, msg_chat_id))

            vals = {'word': word, 'count': 1, 'user_id': msg_user_id, 'chat_id': msg_chat_id}
            q = sqlalchemy.insert(Words).values(vals)
            Dbase.conn.execute(q)

        else:
            q = sqlalchemy.select(Words.count).where(
                Words.word==word, Words.user_id==msg_user_id, Words.chat_id==msg_chat_id)
            db_word_count = Dbase.conn.execute(q).first()[0]

            vals = {'count': db_word_count+1}
            q = sqlalchemy.update(Words).where(
                Words.word==word, Words.user_id==msg_user_id, Words.chat_id==msg_chat_id).values(vals)
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
        .where(Words.chat_id==msg_chat_id)\
        .order_by(-Words.count)\
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
        .order_by(-Words.count)\
        .limit(words_limit)
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


def db_word_stat_like_get(msg_chat_id, input_word):
    """
    Returns 
    * `dict`:
        * `key` input_word: `int` word count or `None`
        * `key` similar_word: `int` word count
        * `key` similar_word...
        * `key` humans_count: `int` how many people said word
    """
    res = {}

    q = sqlalchemy.select(
        Dbase.sq_sum(Words.count))\
        .filter(Words.chat_id==msg_chat_id, Words.word==input_word)
    res[input_word] = Dbase.conn.execute(q).first()[0]

    q = sqlalchemy.select(Words.word)\
        .filter(Words.chat_id==msg_chat_id, Words.word.like('%'+input_word+'%'))
    similar_words = set(i[0] for i in Dbase.conn.execute(q).all())

    for i in similar_words:

        q = sqlalchemy.select(
            Dbase.sq_sum(Words.count))\
            .filter(Words.chat_id==msg_chat_id, Words.word==i)
        res[i] = Dbase.conn.execute(q).first()[0]

    humans_count = 0
    similar_words.add(input_word)

    for i in similar_words:
        q = sqlalchemy.select(Dbase.sq_count(Words.word))\
            .filter(Words.chat_id==msg_chat_id, Words.word==i)
        humans_count += Dbase.conn.execute(q).first()[0]

    res['humans_count'] = humans_count
    return res

