import sqlalchemy
from test_db import *


sq_sum = sqlalchemy.sql.expression.func.sum
sq_count = sqlalchemy.sql.expression.func.count
chat_id = 1

# queries = []
# for user_id in (1, 2):
#     queries.append(
#         sqlalchemy.select(
#             Words.user_id, sq_sum(Words.count), sq_count(Words.word))
#         .filter(
#             Words.user_id==user_id, Words.chat_id==chat_id)
#         )

# query = sqlalchemy.union(*queries)
# res = [dict(i) for i in Dbase.conn.execute(query).fetchall()]


from collections import Counter


def db_words_count(users: dict):
    queries = []

    for k, v in users.items():
        queries.append(
            sqlalchemy.select(Words)
            .filter(Words.user_id == k[0], Words.chat_id == k[1],
            Words.word.in_(v)))

    db_words = [
        dict(i) for i in Dbase.conn.execute(
            sqlalchemy.union_all(*queries)).fetchall()
            ]

    db_count = {}
    for i in db_words:
        user = (i['user_id'], i['chat_id'])
        if not db_count.get(user):
            db_count[user] = {i['word']: i['count']}
        else:
            db_count[user].update({i['word']: i['count']})
    return db_count


def msg_words_count(users: dict):
    users_count = {}
    for k, v in users.items():
        users_count[k] = dict(Counter(v))
    return users_count


def old_words_update(db_words_c: dict, msg_words_c: dict):
    for user, words in db_words_c.items():
        for word in words:
            words[word] = words[word] + msg_words_c[user][word]
    print(db_words_c)
    # here db_update_query


def new_words_insert(db_words_c: dict, msg_words_c: dict):

    new_users_c = {k: v for k, v in msg_words_c.items() if k not in db_words_c}
    old_users = {k: v for k, v in msg_words_c.items() if k not in new_users_c}

    new_words_c = {}
    for user, words in old_users.items():
        tmp = []
        for word, count in words.items():
            if word not in db_words_c[user]:
                tmp.append((word, count))
        new_words_c[user] = dict(tmp)

    print(new_words_c)
    print(new_users_c)

users = {
    (111, 100): ['Вода', 'Кислота', 'Рвота','Тортик', 'Коты', 'Коты', 'Коты', 'Вода','Балашова', 'Пиздец', 'Пиздец', 'Пиздец'],
    (222, 100): ['Гречка', 'Тонна', 'Еда', 'Умка', 'Вода', 'Новое'],
    (111, 300): ['Вода', 'Кислота', 'Рвота','Тортик', 'Коты'],
    }


db_c = db_words_count(users)
msg_c = msg_words_count(users)

old_words_update(db_c, msg_c)
new_words_insert(db_c, msg_c)


# words = {
#     (1, 1): ['Вода', 'Кислота', 'Рвота','Тортик', 'Коты'],
#     (2, 1): ['Гречка', 'Тонна', 'Еда', 'Умка']
#     }


# values_list = []

# for k, v in words.items():
#     for word in v:
#         values_list.append(
#             {'word': word, 'count': 1, 'user_id': k[0], 'chat_id': k[1]}
#             )


# q = sqlalchemy.insert(Words).values(values_list)
# Dbase.conn.execute(q)