import random
import string
import time
from datetime import datetime
from datetime import time as dtime
import cfg
import cv2
import numpy as np
import pymorphy2
import sqlalchemy

from database import Dbase, LiberaModel, Users, Words
from dicts import stop_words


def my_words(msg_user_id, msg_chat_id, msg_username):
    """
    Telegram `/my_words`. 
    Returns text with top 10 words of current user in current chat.
    """
    q = sqlalchemy.select(Words.word, Words.count).where(
        Words.user_id==msg_user_id, Words.chat_id==msg_chat_id).order_by(-Words.count)
    db_words = Dbase.conn.execute(q).fetchall()[:10]
    rowed = ''.join([f'{word}: {count}\n' for word, count in db_words])
    return f'@{msg_username}, ваш топ 10 слов в чате\n\n' + rowed


def chat_words(msg_chat_id, msg_username):
    """
    Telegram `/chat_words`. 
    Returns text with top 10 words in current chat.
    """
    q = sqlalchemy.select(Words.word, Words.count).where(
        Words.chat_id==msg_chat_id).order_by(-Words.count)
    db_words = Dbase.conn.execute(q).fetchall()

    unic_words = set(i[0] for i in db_words)
    result = []

    for u_word in unic_words:
        u_count = 0
        for db_word, db_count in db_words:
            u_count += db_count if u_word == db_word else False
        result.append((u_word, u_count))

    result = tuple(reversed(sorted(result, key=lambda x: x[1])))[:10]
    rowed = ''.join([f'{word}: {count}\n' for word, count in result])
    return f'@{msg_username}, топ 10 слов всех участников в чате\n\n' + rowed


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


def write_db(msg_user_id, msg_chat_id, words_list: words_convert):
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


def check_user(msg_user_id: int, msg_username: str):
    """
    Checks database `Users` table for user by `user_id` from message.
    Creates new record if now exists.
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


def detect_candle(input):
    """
    Returns `True` if candle image detected in current user profile picture.
    Returns `False` if not.
    """
    candle_img = cv2.imread(cfg.candle_img_path, 0)
    usr_picture = cv2.imread(input, 0)

    res = cv2.matchTemplate(usr_picture, candle_img, cv2.TM_CCOEFF_NORMED)
    threshold = 0.95
    loc = np.where(res >= threshold)

    if loc[::-1][1].size > 0:
        return True
    return False


def president_word(words_list: words_convert):
    """
    Returns `image path` if name of Zelensky, Putin or Biden in any word.
    Returns `False` if not found.
    *`word_list`: list of words from `words_convert`
    """
    for word in words_list:
        if cfg.zelensky_name in word:
            return cfg.zelensky_path
        elif cfg.putin_name in word:
            return cfg.putin_path
        elif cfg.biden_name in word:
            return cfg.biden_path
    return False


def top_boltunov(msg_chat_id, msg_username):
    """
    Returns `text` with top 10 users by words count and top 10 users by unique
    words count.
    """
    q = sqlalchemy.select(Users.user_id, Users.user_name)
    db_users = Dbase.conn.execute(q).fetchall()

    user_words = []
    unique = []

    for db_id, db_user_name in db_users:

        q = sqlalchemy.select(Words.count).where(Words.chat_id==msg_chat_id, Words.user_id==db_id)
        words_count = sum(i[0] for i in Dbase.conn.execute(q).fetchall())
        user_words.append((db_user_name, words_count)) if words_count != 0 else False

        q = sqlalchemy.select(Words.word).where(Words.chat_id==msg_chat_id, Words.user_id==db_id)
        words_count = set(i[0] for i in Dbase.conn.execute(q).fetchall())
        words_count = len(words_count)
        unique.append((db_user_name, words_count)) if words_count != 0 else False

    res = []
    for lst in (user_words, unique):
        tmp = sorted(lst, key=lambda x: x[1])
        tmp.reverse()
        tmp = tmp[:10]
        tmp = '\n'.join(f'{i[0]}: {i[1]} слов' for i in tmp)
        res.append(tmp)

    return (
        f'@{msg_username}, топ 10 пиздюшек:\n\n'
        f'{res[0]}\n\n'
        'Топ 10 по уникальным словам:\n\n'
        f'{res[1]}\n'
        )


# unused
def nltk_download(module: str):
    import ssl
    import nltk
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    nltk.download(module)
