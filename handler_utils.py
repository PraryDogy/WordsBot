import cfg
import cv2
import numpy as np
import sqlalchemy
from datetime import datetime
from database import Dbase, Users, Words
from utils import db_username_get, db_usernames_get, db_words_get, db_userid_get


def get_user_words(msg_chat_id, msg_username, msg_args: str):
    """
    Returns text with top 10 words of user in current chat.
    """
    if msg_args:
        msg_args = msg_args.replace('@', '')
        username = db_username_get(msg_args)
    else:
        username = db_username_get(msg_username)

    if username:
        usr_id = db_userid_get(username)
    else:
        return 'Нет данных о пользователе'

    q = sqlalchemy.select(Words.word, Words.count).where(
        Words.user_id==usr_id, Words.chat_id==msg_chat_id).order_by(-Words.count)
    db_words = Dbase.conn.execute(q).fetchall()[:10]
    rowed = ''.join([f'{word}: {count}\n' for word, count in db_words])
    
    if msg_username == username:
        return f'@{msg_username}, ваш топ 10 слов в чате\n\n' + rowed
    else:
        return f'@{msg_username}, топ 10 слов в чате пользователя {username}\n\n' + rowed


def chat_words(msg_chat_id, msg_username):
    """
    Telegram `/chat_words`. 
    Returns text with top 10 words in current chat.
    """
    db_words = db_words_get(msg_chat_id)
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


def get_usr_t(msg_usr_name, msg_args: str):
    if msg_args:
        print(msg_args)
        msg_args = msg_args.replace('@', '')
    else:
        return 'Пример команды: "/last_time @имя_пользователя"'

    username = db_username_get(msg_args)
    if not username:
        return 'Нет данных о таком пользователе'

    select_time = sqlalchemy.select(Users.last_time).where(Users.user_name==username)
    db_time = Dbase.conn.execute(select_time).first()[0]
    
    if db_time is None:
        return 'Нет данных о последнем сообщении'

    msg_time = datetime.strptime(db_time, '%Y-%m-%d %H:%M:%S')
    msg_time = msg_time.strftime('%H:%M %d.%m.%Y')

    msg = f'@{msg_usr_name}, пользователь {username} последний раз писал {msg_time}'
    return msg


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


def top_boltunov(msg_chat_id, msg_username):
    """
    Returns `text` with top 10 users by words count and top 10 users by unique
    words count.
    """
    user_words = []
    unique = []

    for db_id, db_user_name in db_usernames_get():

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
# def nltk_download(module: str):
#     import ssl
#     import nltk
#     try:
#         _create_unverified_https_context = ssl._create_unverified_context
#     except AttributeError:
#         pass
#     else:
#         ssl._create_default_https_context = _create_unverified_https_context
#     nltk.download(module)
