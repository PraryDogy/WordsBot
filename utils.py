import random
import string
import time
from datetime import datetime
from datetime import time as dtime

import cv2
import numpy as np
import pymorphy2
import sqlalchemy

from database import Dbase, Libera, Users, Words
from dicts import stop_words, libera, no_libera


def summarize_words(input: tuple):
    """
    Summarizes count of same words
    Returns list of unique words with new count
    """
    unic_words = set(i[0] for i in input)
    result = []
    for word in unic_words:
        counter = 0
        for w, c in input:
            counter += c if word == w else False
        result.append((word, counter))
    return tuple(reversed(sorted(result, key=lambda x: x[1])))


def my_words(msg_user_id, msg_chat_id, msg_username):
    """
    For command /my_words
    """
    q = sqlalchemy.select(Words.word, Words.count).where(
        Words.user_id==msg_user_id, Words.chat_id==msg_chat_id).order_by(-Words.count)
    db_words = Dbase.conn.execute(q).fetchall()[:10]
    rowed = ''.join([f'{word}: {count}\n' for word, count in db_words])
    return f'@{msg_username}, ваш топ 10 слов в чате\n\n' + rowed


def chat_words(msg_chat_id, msg_username):
    """
    For command /chat_words
    """
    q = sqlalchemy.select(Words.word, Words.count).where(
        Words.chat_id==msg_chat_id).order_by(-Words.count)
    db_words = Dbase.conn.execute(q).fetchall()
    sorted = summarize_words(db_words)[:10]
    rowed = ''.join([f'{word}: {count}\n' for word, count in sorted])
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
    rem_whitespaces = [i.replace(' ', '') for i in words_list]
    lower_cases = [i.lower() for i in rem_whitespaces]
    
    lemm_words = lemmatize_text(lower_cases)

    return tuple(i for i in lemm_words if i not in stop_words)


def write_db(msg_user_id, msg_chat_id, msg_words):
    """
    Gets all user's words with all chats ids  from database
    If word from input words list not in database words list - adds new row
    If word in database words list but has other chat id - adds new row
    If word in database words list and has the same chat id - updates word counter
    """
    msg_words = words_convert(msg_words)

    query = sqlalchemy.select(Words.word, Words.chat_id).where(Words.user_id==msg_user_id)
    db_user_words = list(Dbase.conn.execute(query).fetchall())
    new_words = []

    for word in msg_words:
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


def check_user(msg_user_id: int, msg_user_name: str):
    get_user = sqlalchemy.select(
        Users.user_id, Users.user_name).filter(Users.user_id == msg_user_id)
    db_user = Dbase.conn.execute(get_user).first()
    
    if db_user is not None:

        db_usr_id, db_usr_name = db_user

        if db_usr_name != msg_user_name:

            vals = {'user_name': msg_user_name}
            new_name = sqlalchemy.update(Users).where(
                Users.user_id==db_usr_id).values(vals)
            Dbase.conn.execute(new_name)
    else:
        vals = {'user_id': msg_user_id, 'user_name': msg_user_name}
        new_user = sqlalchemy.insert(Users).values(vals)
        Dbase.conn.execute(new_user)


def nltk_download(module: str):
    import ssl

    import nltk
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    nltk.download('stopwords')


def den_light(input):
    """
    True = no light
    """
    candle_piece = cv2.imread('./candles/candle_piece_640.png', 0)
    img = cv2.imread(input, 0)

    res = cv2.matchTemplate(img, candle_piece, cv2.TM_CCOEFF_NORMED)
    threshold = 0.95
    loc = np.where(res >= threshold)

    if loc[::-1][1].size > 0:
        print('true')
        return True

    return False


def libera_words(percent):
    if percent >= 50:
        return random.choice(libera)
    else:
        return random.choice(no_libera)


def libera_func(msg_user_id, msg_username):
    hours24 = 86400
    now = int(time.time())

    percent = random.randint(0, 100)

    q = sqlalchemy.select(Libera).where(Libera.user_id==msg_user_id)
    usr_check = bool(Dbase.conn.execute(q).first())
    if not usr_check:

        vals = {'percent':percent, 'time': now, 'user_id': msg_user_id}
        q = sqlalchemy.insert(Libera).values(vals)
        Dbase.conn.execute(q)
        return (
            f'Вы, @{msg_username}, либеральны на {percent}%'
            f'\n{libera_words(percent)}'
            )

    else:

        q = sqlalchemy.select(Libera.time).where(Libera.user_id==msg_user_id)
        db_usr_time = Dbase.conn.execute(q).first()[0]
        if db_usr_time + hours24 < now:

            vals = {'percent':percent, 'time': now}
            q = sqlalchemy.update(Libera).where(Libera.user_id==msg_user_id).values(vals)
            Dbase.conn.execute(q)
            return (
                f'Вы, @{msg_username}, либеральны на {percent}%'
                f'\n{libera_words(percent)}'
                )

        else:
            q = sqlalchemy.select(Libera.percent).where(Libera.user_id==msg_user_id)
            usr_percent = Dbase.conn.execute(q).first()[0]

            future_t = db_usr_time + hours24
            midnight = datetime.combine(datetime.today(), dtime.max).timestamp()
            if midnight - future_t < 0:
                today_tomorr = 'завтра'
            else:
                today_tomorr = 'завтра'

            future_t = datetime.fromtimestamp(future_t)
            future_t = future_t.strftime('%H:%M')

            return (
                f'Вы, @{msg_username}, либеральны на {usr_percent}%'
                f'\n{libera_words(usr_percent)}'
                f'\nОбновить можно {today_tomorr} в {future_t}'
                )