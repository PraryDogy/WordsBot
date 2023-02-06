import itertools
from collections import Counter
from datetime import datetime
from functools import wraps
from time import time

import sqlalchemy
from aiogram import types

from database import Dbase, Users, Words


def testing(name):
    import timeit
    return timeit.repeat(
        f"for x in range(100): {name}()",
        f"from __main__ import {name}",
        number=10
        )


def split_link():
    import clipboard
    max = 50
    url = clipboard.paste()
    
    chunks = [url[i:i+max] for i in range(0, len(url), max)]
    chunks = (f"'{i}'" for i in chunks)
    url = "\n".join(chunks)

    clipboard.copy(url)



# def load_times_db(self):
#     queries = (
#         sqlalchemy.select(Users.time)
#         .filter(Users.user_id==user_id)

#     for (user_id, chat_id), times in users_times.items()
#     )

#     SQL_MAX = 300
#     q_chunks = [
#         queries[i:i+SQL_MAX]
#         for i in range(0, len(queries), SQL_MAX)
#         ]

#     results = [
#         (
#             Dbase.conn.execute(sqlalchemy.union_all(*q))
#             .mappings()
#             .fetchall()
#             )
#         for q in q_chunks
#         ]

#     return list(itertools.chain.from_iterable(results))

import bot_config
from utilites.main import sql_unions
from datetime import datetime


users_times: dict = {
    bot_config.evlosh: [datetime.today().replace(microsecond=0) for i in range(3)],
    345804134: [datetime.today().replace(microsecond=0) for i in range(3)],
    }

class TimesWrite:
    def __init__(self) -> None:
        self.db_times: list = self.load_times_db()
        self.stringed = self.string_users_times()
        self.merged: dict = self.merge_times()
        print(self.merged)

    def load_times_db(self):
        queries = [
            sqlalchemy.select(Users.user_id, Users.times)
            .filter(Users.user_id==user_id)

            for user_id in users_times
        ]

        return sql_unions(queries)

    def string_users_times(self):
        return {
            user_id: ','.join((str(i) for i in times))
            for user_id, times in users_times.items()
        }

    def merge_times(self):
        return {
            print(k, v)
            for user_dict in self.db_times
            for k, v in user_dict.items()
        }

# TimesWrite()
