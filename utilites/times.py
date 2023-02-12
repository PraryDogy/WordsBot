from . import Dbase, Times, datetime, json, sqlalchemy, types, wraps

__all__ = (
    "times_db_update_force",
    "dec_times_db_update_force",
    "times_dict_append",
    )

dict_message: dict = {}


class __UpdateTimes:
    def __init__(self):
        self.year = datetime.today().year

        self.__db_times = self.load_times_db()
        self.db_json_loaded = self.times_db_json_loads()

        self.merged = self.merge_times()
        self.new = self.new_users()

        self.update_db() if self.merged else False
        self.insert_db() if self.new else False

    def load_times_db(self):
        """
        out: [ (user_id, chat_id, [str datetimes]), ... ]
        """
        queries = [
            sqlalchemy.select(
                Times.user_id,
                Times.chat_id,
                Times.times_list
                )
            .filter(
                Times.user_id==user_id,
                Times.chat_id==chat_id,
                Times.year==self.year
                )
            for user_id, chat_id in dict_message.keys()
            ]

        return Dbase.conn.execute(
            sqlalchemy.union_all(*queries)
            ).all()

    def times_db_json_loads(self):
        """
        out: [ (user_id, chat_id, [json loads datetimes]), ... ]
        """
        return [
            (user_id, chat_id, json.loads(times_list))
            for user_id, chat_id, times_list in self.__db_times
            ]

    def merge_times(self):
        """
        in: [ (user_id, chat_id, [datetimes]), ... ]
        out: [ (user_id, chat_id,
        [datetimes] + [datetimes from dict_message]), ... ]
        """
        return [
            (
                user_id,
                chat_id,
                dict_message[(user_id, chat_id)] + times_list
                )
            for user_id, chat_id, times_list in self.db_json_loaded
            ]

    def new_users(self):
        """
        out [ (user_id, chat_id, [datetimes]), ... ] if user not in db
        """
        return [
            (
                user_id,
                chat_id,
                times_list
                )
            for (user_id, chat_id), times_list in dict_message.items()
            if (user_id, chat_id) not in (
                (user_id, chat_id)
                for user_id, chat_id, _ in self.merged
                )
                ]

    def update_db(self):
        vals = [
            {
                "b_user_id": user_id,
                "b_chat_id": chat_id,
                "b_year": self.year,
                "b_times_list": json.dumps(times_list, default=str, indent=1)
                }
            for user_id, chat_id, times_list in self.merged
            ]

        q = (
            sqlalchemy.update(Times)
            .values({
                'times_list': sqlalchemy.bindparam("b_times_list")
                })
            .filter(
                Times.user_id == sqlalchemy.bindparam("b_user_id"),
                Times.chat_id == sqlalchemy.bindparam("b_chat_id"),
                Times.year == sqlalchemy.bindparam("b_year"),
                )
            )

        Dbase.conn.execute(q, vals)

    def insert_db(self):
        vals = [
            {
                "b_user_id": user_id,
                "b_chat_id": chat_id,
                "b_year": self.year,
                "b_times_list": json.dumps(times_list, default=str, indent=1)
                }
            for user_id, chat_id, times_list in self.new
            ]

        q = (
            sqlalchemy.insert(Times)
            .values({
                "user_id": sqlalchemy.bindparam("b_user_id"),
                "chat_id": sqlalchemy.bindparam("b_chat_id"),
                "times_list": sqlalchemy.bindparam("b_times_list"),
                "year": sqlalchemy.bindparam("b_year")
                })
            )

        Dbase.conn.execute(q, vals)


def __times_dict_append(message: types.Message):
    today = datetime.today().replace(microsecond=0)
    user = (message.from_user.id, message.chat.id)

    if not dict_message.get(user):
        dict_message[user] = [today]
    else:
        dict_message[user].append(today)


def __times_db_update():
    __UpdateTimes()
    dict_message.clear()


def times_dict_append(message: types.Message):
    """
    Appends datetime.today to list of times for user_id
    when user_id send any text message
    """
    __times_dict_append(message)


def times_db_update_force():
    """
    Force update list of times in database
    for any user_id who send text messages
    """
    __times_db_update() if dict_message else False


def dec_times_db_update_force(func):
    """
    Force update list of times in database
    for any user_id who send text messages
    """

    @wraps(func)
    def wrapper(message: types.Message):
        __times_db_update() if dict_message else False
        return func(message)

    return wrapper