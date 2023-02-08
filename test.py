from database import *
import bot_config
import sqlalchemy
from datetime import datetime
import random
from dicts import *
import json
from utilites import sql_unions


dict_message = {
    (1, 1): ["time" for i in range(3)],
    (2, 2): ["time" for i in range(3)], # new user
    }


class UpdateTimes:
    def __init__(self) -> None:
        self.__db_times: list = self.load_times_db()
        self.dict_db: dict = self.times_db_from_json()

        self.merged: tuple = self.merge_times()
        self.new: tuple = self.new_users()

        self.update_db() if self.merged else False
        self.insert_db() if self.new else False

    def load_times_db(self):
        """Returns list of dicts"""
        queries = [
            sqlalchemy.select(Times.user_id, Times.chat_id, Times.times_list)
            .filter(Times.user_id==user_id, Times.chat_id==chat_id)
            for user_id, chat_id in dict_message.keys()
            ]
        return sql_unions(queries)

    def times_db_from_json(self):
        return {
            (x["user_id"], x["chat_id"]): json.loads(x["times_list"])
            for x in self.__db_times
            }

    def merge_times(self):
        return [
            {user: dict_message[user] + times_list}
            for user, times_list in self.dict_db.items()
            ]

    def new_users(self):
        return [
            {user: times_list}
            for user, times_list in dict_message.items()
            if not self.dict_db.get(user)
        ]

    def update_db(self):
        vals = [
            {
                "b_user_id": user_id,
                "b_chat_id": chat_id,
                "b_times_list": json.dumps(times_list)
                }
            for x in self.merged
            for (user_id, chat_id), times_list in x.items()
            ]

        q = (
            sqlalchemy.update(Times)
            .values({'times_list': sqlalchemy.bindparam("b_times_list")})
            .filter(
                Times.user_id==sqlalchemy.bindparam("b_user_id"),
                Times.user_id==sqlalchemy.bindparam("b_user_id")
                )
            )

        Dbase.conn.execute(q, vals)

    def insert_db(self):
        vals = [
            {
                "b_user_id": user_id,
                "b_chat_id": chat_id,
                "b_times_list": json.dumps(times_list)
                }
            for x in self.new
            for (user_id, chat_id), times_list in x.items()
            ]

        q = (
            sqlalchemy.insert(Times)
            .values({
                "user_id": sqlalchemy.bindparam("b_user_id"),
                "chat_id": sqlalchemy.bindparam("b_chat_id"),
                'times_list': sqlalchemy.bindparam("b_times_list")
                })
            )

        Dbase.conn.execute(q, vals)



UpdateTimes()