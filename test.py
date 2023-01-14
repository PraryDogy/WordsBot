import json
from datetime import datetime

import cv2
import numpy as np
import sqlalchemy

import cfg
from database import Dbase, Words
from database_queries import (db_all_usernames_get, db_chat_words_get,
                              db_user_get, db_user_time_get, db_user_words_get,
                              db_word_stat_get)
from text_analyser import get_nouns, normalize_word


def top_boltunov(msg_chat_id, msg_username):
    """
    Returns `text` with top 10 users by words count and top 10 users by unique
    words count.
    """
    user_words = []
    msg = []

    for db_user_id, db_user_name in db_all_usernames_get():

        q = sqlalchemy.select(
            Dbase.sq_sum(Words.count),
            Dbase.sq_count(Words.word))\
            .where(Words.user_id==db_user_id, Words.chat_id==msg_chat_id)
        all_words_c, uniq_words_c = Dbase.conn.execute(q).first()

        uniq = int(100*(uniq_words_c/all_words_c)) if uniq_words_c else False
        user_words.append((db_user_name, all_words_c, uniq)) if all_words_c else False

    user_words = sorted(user_words, key=lambda i: i[1], reverse=1)

    msg.append(f'@{msg_username}, топ 10 пиздюшек.')
    msg.append('Имя, количество слов, процент уникальных:\n')
    for name, words, perc in user_words[:10]:
        msg.append(f'{name}: {words}, {perc}%')

    return '\n'.join(msg)
