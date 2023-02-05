from datetime import datetime, timedelta
from functools import wraps

import sqlalchemy
from aiogram import types

from database import Dbase, Users


class UserData:
    def __init__(self, message: types.Message):
        self.user_id = message.from_user.id
        self.user_name = message.from_user.username
        self.today = datetime.today().replace(microsecond=0)

    def get_db_user_data(self):
        q = (
            sqlalchemy.select(Users)
            .filter(Users.user_id == self.user_id)
            )
        try:
            return dict(Dbase.conn.execute(q).first())
        except TypeError:
            return False

    def update_db_user_name(self, user: dict):
        if user['user_name'] != self.user_name:
            q = (
                sqlalchemy.update(Users)
                .filter(Users.user_id==user['user_id'])
                .values({'user_name': self.user_name})
                )
            Dbase.conn.execute(q)

    def create_db_user(self):
        new_user = {
                'user_id': self.user_id,
                'user_name': self.user_name,
                'user_time': self.today - timedelta(days=1),
                'times': self.today
                }

        Dbase.conn.execute(
            sqlalchemy.insert(Users)
            .values(new_user)
            )

    def update_db_user_time(self, today: datetime):
        q = (
            sqlalchemy.update(Users)
            .filter(Users.user_id==self.user_id)
            .values({'user_time': today})
            )
        Dbase.conn.execute(q)


def dec_update_user(func):

    @wraps(func)
    def wrapper(message: types.message):

        user = UserData(message)
        user_data = user.get_db_user_data()

        if not user_data:
            user.create_db_user()

        else:
            user.update_db_user_name(user_data)

        return func(message)
    return wrapper


