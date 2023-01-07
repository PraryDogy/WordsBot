import string
from datetime import datetime

import pymorphy2
import sqlalchemy

from database import Dbase, Users, Words
from dicts import stop_words

lemmatizer = pymorphy2.MorphAnalyzer()
def lemmatize_text(tokens):
    lem_words = []
    for word in tokens:
        lem_words.append(lemmatizer.parse(word)[0].normal_form)
    return lem_words


def words_convert(text: str):
    """
    Converts telegram message to words list
    - removes puntkuation, whitespaces and newlines
    - all words are lowercase
    - removes stop words
    - lemmatize words
    """
    remove_punktuation = text.translate(text.maketrans('', '', string.punctuation))
    remove_newlines = remove_punktuation.replace('\n', ' ')
    
    words_list = remove_newlines.split(' ')
    rem_whitespaces = tuple(i.replace(' ', '') for i in words_list)
    lower_cases = tuple(i.lower() for i in rem_whitespaces)
    link_rem = tuple(i for i in lower_cases if 'http' not in i)
    lemm_words = lemmatize_text(link_rem)

    return tuple(i for i in lemm_words if i not in stop_words)


def db_words_record(msg_user_id, msg_chat_id, words_list: words_convert):
    """
    Gets all user's words with all chats ids  from database
    If word from input words list not in database words list - adds new row
    If word in database words list but has other chat id - adds new row
    If word in database words list and has the same chat id - updates word counter
    """
    query = sqlalchemy.select(Words.word, Words.chat_id).where(Words.user_id==msg_user_id)
    db_user_words = list(Dbase.conn.execute(query).fetchall())
    new_words = []

    for word in words_list:
        if (
            (word, msg_chat_id) not in db_user_words
            and
            (word, msg_chat_id) not in new_words):

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


def db_time_record(msg_usr_id):
    vals = {'last_time': datetime.today().replace(microsecond=0)}
    q = sqlalchemy.update(Users).where(Users.user_id==msg_usr_id).values(vals)
    Dbase.conn.execute(q)


def db_username_get(wished_usr_name: str):
    """
    Returns username of False.
    """
    q = sqlalchemy.select(Users.user_name)
    all_usernames = tuple(i[0] for i in Dbase.conn.execute(q).fetchall())
    all_usernames = tuple(i for i in all_usernames if i is not None)

    true_name = False
    for i in all_usernames:
        if i.lower() == wished_usr_name.lower():
            true_name = i

    if not true_name:
        return False

    return true_name


def db_userid_get(input_username):
    """
    Returns user_id by username
    """
    q = sqlalchemy.select(Users.user_id).where(Users.user_name==input_username)
    return Dbase.conn.execute(q).first()[0]


def db_all_usernames_get():
    q = sqlalchemy.select(Users.user_id, Users.user_name)
    return Dbase.conn.execute(q).fetchall()


def db_chat_usernames_get(msg_chat_id):
    q = sqlalchemy.select(Words.user_id).where(Words.chat_id==msg_chat_id)
    ids = Dbase.conn.execute(q).fetchall()
    ids = set(tuple(i[0] for i in ids))

    usernames = []
    for i in ids:
        q = sqlalchemy.select(Users.user_name).where(Users.user_id==i)
        usernames.append(Dbase.conn.execute(q).first()[0])
    
    return usernames


def db_words_get(msg_chat_id):
    q = sqlalchemy.select(Words.word, Words.count).where(
        Words.chat_id==msg_chat_id).order_by(-Words.count)
    return Dbase.conn.execute(q).fetchall()