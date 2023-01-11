from datetime import datetime

import cv2
import numpy as np
import sqlalchemy

import cfg
from database import Dbase, Words
from database_queries import (db_all_usernames_get, db_chat_words_get,
                              db_user_get, db_user_time_get, db_user_words_get,
                              db_word_stat_get, db_word_stat_like_get)
from text_analyser import get_nouns, normalize_word


def user_words_top(msg_chat_id, msg_username, msg_args: str):
    """
    Returns text with top 10 words of user in current chat.
    """
    if msg_args:
        user = db_user_get(msg_args.replace('@', ''))
    else:
        user = db_user_get(msg_username)

    if not user:
        return 'Нет данных о пользователе'

    db_words = db_user_words_get(user[0], msg_chat_id, 500)
    db_nouns = get_nouns(db_words)[:10]

    rowed_words = ''.join([f'{word}: {count}\n' for word, count in db_words[:10]])
    rowed_nouns = ''.join([f'{word}: {count}\n' for word, count in db_nouns])

    if not msg_args:
        return f'@{msg_username}, ваш топ 10 слов в чате\
                \n\n{rowed_words}\
                \nТоп 10 существительных:\
                \n\n{rowed_nouns}'
    else:
        return f'@{msg_username}, топ 10 слов в чате пользователя {user[1]}\
                \n\n{rowed_words}\
                \nТоп 10 существительных:\
                \n\n{rowed_nouns}'


def chat_words_top(msg_chat_id, msg_username):
    """
    Telegram `/chat_words`. 
    Returns text with top 10 words in current chat.
    """
    db_words = db_chat_words_get(msg_chat_id, 500)
    db_nouns = get_nouns(db_words)

    best_words = []
    best_nouns = []

    for u_word in set(i[0] for i in db_nouns):
        macth_list = tuple((word, id) for word, id in db_words if u_word == word)
        best_nouns.append((u_word, sum([i[1] for i in macth_list])))

    for u_word in set(i[0] for i in db_words):
        macth_list = tuple((word, id) for word, id in db_words if u_word == word)
        best_words.append((u_word, sum([i[1] for i in macth_list])))

    sorted_words = sorted(best_words, key = lambda x: x[1], reverse=1)[:10]
    sorted_nouns = sorted(best_nouns, key = lambda x: x[1], reverse=1)[:10]

    str_words = ''.join([f'{word}: {count}\n' for word, count in sorted_words])
    str_nouns = ''.join([f'{noun}: {count}\n' for noun, count in sorted_nouns])

    return f'@{msg_username}, топ 10 слов чата\
            \n\n{str_words}\
            \nТоп 10 существительных чата:\
            \n\n{str_nouns}'


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

    for db_user_id, db_user_name in db_all_usernames_get():

        q = sqlalchemy.select(
            Dbase.sq_sum(Words.count),
            Dbase.sq_count(Words.word))\
            .where(Words.user_id==db_user_id, Words.chat_id==msg_chat_id)
        all_words_c, uniq_words_c = Dbase.conn.execute(q).first()

        user_words.append((db_user_name, all_words_c)) if all_words_c else False
        unique.append((db_user_name, uniq_words_c)) if uniq_words_c else False

    res = []
    for words_list in (user_words, unique):
        tmp = sorted(words_list, key=lambda x: x[1], reverse=1)[:10]
        res.append('\n'.join(f'{i[0]}: {i[1]} слов' for i in tmp))

    return (
        f'@{msg_username}, топ 10 пиздюшек:\n\n'
        f'{res[0]}\n\n'
        'Топ 10 по уникальным словам:\n\n'
        f'{res[1]}\n'
        )


def word_stat(msg_chat_id, args: str):
    if not args:
        return 'Пример команды /word_stat слово.'

    normalized_word = normalize_word(args).lower()
    
    word_analyse_normalized = db_word_stat_like_get(msg_chat_id, normalized_word)
    word_analyse_args = db_word_stat_like_get(msg_chat_id, args.lower())

    if len(word_analyse_normalized) > len(word_analyse_args):
        word_analyse = word_analyse_normalized
    else:
        word_analyse = word_analyse_args
        normalized_word = args

    lines = []

    if not word_analyse[normalized_word]:
        lines.append(f'Нет данных о слове {args}.')
        word_analyse[normalized_word] = 0

    else:
        lines.append(f'Статистика слова {args}:')

    similar_words = ", ".join(list(word_analyse.keys())[1:-1])

    if similar_words:
        lines.append(f'Похожие слова: {similar_words}')

        all_words_count = sum(list(word_analyse.values())[:-1])
        lines.append(f'Было сказано: {all_words_count} раз.')

    else:
        lines.append(f'Было сказано: {word_analyse[normalized_word]} раз')

    lines.append(f'Это слово сказало {word_analyse["humans_count"]} человек.')

    lines.append('Попробуйте написать корень слова для лучшего результата.')

    return '\n'.join(lines)


def get_usr_t(msg_usr_name, msg_args: str):
    if msg_args:
        msg_args = msg_args.replace('@', '')
    else:
        return 'Пример команды: /last_time @имя_пользователя'

    username = db_user_get(msg_args)[0]
    if not username:
        return 'Нет данных о таком пользователе'

    db_time = db_user_time_get(username)
    
    if not db_time:
        return 'Нет данных о последнем сообщении'

    msg_time = datetime.strptime(db_time[0], '%Y-%m-%d %H:%M:%S')
    msg_time = msg_time.strftime('%H:%M %d.%m.%Y')

    msg = f'@{msg_usr_name}, пользователь {username} последний раз писал {msg_time}'
    return msg
