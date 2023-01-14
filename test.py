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


def word_stat(msg_chat_id, args: str):
    if not args:
        return 'Пример команды /word_stat слово.'

    args = args.lower()
    word_variants = []
    word_stats = []

    word_variants.append(args)
    word_variants.append(normalize_word(args))
    word_variants.append(args[:-1] if len(args) > 3 else args)
    word_variants.append(args[:-2] if len(args) > 5 else args)

    for i in set(word_variants):
        res = db_word_stat_get(msg_chat_id, i)
        [word_stats.append(res) if res else False]

    if not word_stats:
        return 'Нет данных о таком слове.'

    maxi = max(*word_stats) if len(word_stats) > 1 else word_stats[0]

    msg_list = []
    msg_list.append(f'Статистика слова {args}.')

    similar_words = ", ".join(sorted(maxi[0]))

    if similar_words:
        msg_list.append(f'Похожие слова: {similar_words}.')

    msg_list.append(f'Было сказано: {maxi[1]} раз.')
    msg_list.append(f'Эти слова сказало {maxi[2]} человек.')
    msg_list.append('Попробуйте написать корень слова для лучшего результата.')

    return '\n'.join(msg_list)

a = word_stat(cfg.heli, 'Лапута')

print(a)