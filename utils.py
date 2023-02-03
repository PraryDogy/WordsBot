from datetime import datetime, timedelta

import sqlalchemy

from database import Dbase, Users


class UserData:
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name
        self.today = datetime.today().replace(microsecond=0)

    def __user_get(self):
        q = (
            sqlalchemy.select(Users)
            .filter(Users.user_id == self.user_id)
            )
        try:
            return dict(Dbase.conn.execute(q).first())
        except TypeError:
            return False

    def __user_update_name(self, user: dict):
        if user['user_name'] != self.user_name:
            q = (
                sqlalchemy.update(Users)
                .filter(Users.user_id==user['user_id'])
                .values({'user_name': self.user_name})
                )
            Dbase.conn.execute(q)

    def __user_create(self):
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
        return new_user

    def user_data_get(self):
        user = self.__user_get()

        if not user:
            return self.__user_create()
        else:
            self.__user_update_name(user)

        return user

    def user_update_time(user_id: int, today: datetime):
        q = (
            sqlalchemy.update(Users)
            .filter(Users.user_id==user_id)
            .values({'user_time': today})
            )
        Dbase.conn.execute(q)