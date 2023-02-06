import itertools
from collections import Counter
from datetime import datetime
from functools import wraps
from time import time

import sqlalchemy
from aiogram import types

import bot_config
from database import Dbase, Users, Words

from .main import sql_unions

timer: time = time()
users_times: dict = {}

class TimesWrite:
    def __init__(self) -> None:
        self.db_times = self.load_times_db()
        self.add_times()

    def load_times_db(self):
        queries = [
            sqlalchemy.select(Users.user_id, Users.times)
            .filter(Users.user_id==user_id)

        for (user_id, chat_id) in users_times
        ]

        return sql_unions(queries)

    def add_times(self):
        for user in users_times:
            print(users_times[user])


def times_append(message: types.Message):
    global timer

    today = datetime.today().replace(microsecond=0)
    if not users_times.get(message.from_user.id):
        users_times[message.from_user.id] = [today]
    else:
        users_times[message.from_user.id].append(today)
    
    if time() - timer >= 3600:
        TimesWrite()
        timer = time()
        users_times.clear()


def dec_times_append(func):

    @wraps(func)
    def wrapper(message: types.Message):
        times_append(message)
        print(users_times)
        return func(message)

    return wrapper


def dec_times_write(func):
    
    @wraps(func)
    def wrapper(message: types.Message):
        global timer
        TimesWrite()
        timer = time()
        users_times.clear()
        return func(message)

    return wrapper