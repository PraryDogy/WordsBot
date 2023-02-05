import itertools
from collections import Counter
from functools import wraps
from time import time

import sqlalchemy
from aiogram import types
from datetime import datetime
from database import Dbase, Words

timer: time = time()
users_times: dict = {}


class TimesWrite:
    def __init__(self) -> None:
        pass


def times_append(message: types.Message):
    user = (message.from_user.id, message.chat.id)
    today = datetime.today().replace(microsecond=0)
    if not users_times.get(user):
        users_times[user] = list(today)
    else:
        users_times[user].append(today)


def dec_times_append(func):

    @wraps(func)
    def wrapper(message: types.Message):
        TimesWrite()

        print(users_times)

        return func(message)

    return wrapper