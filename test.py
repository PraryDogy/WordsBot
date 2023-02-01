# from chatgpt_wrapper import ChatGPT


# def gpt():
#     bot = ChatGPT()
#     return bot.ask("Когда появился человек?")



import itertools

import sqlalchemy

from test_db import Dbase, Users, Words


def db_words_get(users: dict):
    """
    returns: `list`( `dict`(user_id, chat_id, word, count) )
    """
    queries = [
        sqlalchemy.select(
            Words.user_id, Words.chat_id, Words.word, Words.count
            )
        .filter(
            Words.user_id == user_id, Words.chat_id == chat_id,
            Words.word == w
            )
        for (user_id, chat_id), words in users.items()
        for w in words
        ]

    SQL_MAX = 300
    q_chunks = [queries[i:i+SQL_MAX] for i in range(0, len(queries), SQL_MAX)]

    results = [
        Dbase.conn.execute(sqlalchemy.union_all(*q)).mappings().fetchall()
        for q in q_chunks
        ]

    return list(itertools.chain.from_iterable(results))


# users = {(1, 2): ['hui' for i in range (1000)]}
# a = db_words_get(users)


# for a, b in enumerate(a):
#     print(a, b)

