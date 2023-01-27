from collections import Counter

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert

from test_db import *

sq_sum = sqlalchemy.sql.expression.func.sum
sq_count = sqlalchemy.sql.expression.func.count
session = Session(Dbase.engine)


def db_words_count(users: dict):
    queries = [
        sqlalchemy.select(Words)
        .filter(Words.user_id == k[0], Words.chat_id == k[1],Words.word.in_(v))
        for k, v in users.items()
        ]

    result = [
        dict(i) for i in Dbase.conn.execute(
        sqlalchemy.union_all(*queries)).fetchall()
        ]

    db_count = {}

    for i in result:
        user = (i['user_id'], i['chat_id'])
        if not db_count.get(user):
            db_count[user] = {i['word']: i['count']}
        else:
            db_count[user].update({i['word']: i['count']})

    return db_count


def msg_words_count(users: dict):
    return {
        k: dict(Counter(v))
        for k, v in users.items()
        }


def old_words_update(db_words_c: dict, msg_words_c: dict):
    for user, words in db_words_c.items():
        for word in words:
            words[word] = words[word] + msg_words_c[user][word]
    # here db_update_query


def new_words_insert(db_words_c: dict, msg_words_c: dict):

    msg_new_users = {k: v for k, v in msg_words_c.items() if k not in db_words_c}
    msg_old_users = {k: v for k, v in msg_words_c.items() if k not in msg_new_users}

    new_words_c = {}
    for user, words in msg_old_users.items():
        new_words = [
            (word, count)
            for word, count in words.items()
            if word not in db_words_c[user]
            ]
        new_words_c[user] = dict(new_words)

    print(new_words_c)


users = {
    (111, 100): ['Вода', 'Кислота', 'Рвота','Тортик', 'Коты', 'Коты', 'Коты', 'Вода','Балашова', 'Пиздец', 'Пиздец', 'Пиздец'],
    (222, 100): ['Гречка', 'Тонна', 'Еда', 'Умка', 'Вода', 'Новое'],
    (111, 300): ['Вода', 'Кислота', 'Рвота','Тортик', 'Коты'],
    }


db_c = db_words_count(users)
msg_c = msg_words_count(users)

old_words_update(db_c, msg_c)
new_words_insert(db_c, msg_c)

