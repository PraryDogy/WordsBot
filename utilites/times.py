from . import (Dbase, Users, datetime, json, sql_unions, sqlalchemy, time,
               types, wraps)

__all__ = (
    "dec_times_update_force",
    "dec_times_update_timer",
    "dec_times_append",
    )

timer: time = time()
users_times: dict = {}


class UpdateTimes:
    def __init__(self) -> None:
        self.db_times: list = self.load_times_db()
        self.deserialized_db: dict = self.deserialize_times_db()
        self.serialized_users: dict = self.serialize_users_times()
        self.merged: tuple = self.merge_times()

        self.update_db()

    def load_times_db(self):
        queries = [
            sqlalchemy.select(Users.user_id, Users.times)
            .filter(Users.user_id==user_id)
            for user_id in users_times
            ]
        return sql_unions(queries)

    def deserialize_times_db(self):
        return {
            dicts["user_id"]:
            json.loads(dicts["times"]) if dicts["times"] else []
            for dicts in self.db_times
            }

    def serialize_users_times(self):
        return {
            id: [str(i) for i in times]
            for id, times in users_times.items()
            }

    def merge_times(self):
        return (
            (id, json.dumps(self.serialized_users[id] + times))
            for id, times in self.deserialized_db.items()
            )

    def update_db(self):
        vals = [
            {"b_user_id": user_id, "b_times": times}
            for user_id, times in self.merged
            ]

        q = (
            sqlalchemy.update(Users)
            .values({'times': sqlalchemy.bindparam("b_times")})
            .filter(Users.user_id==sqlalchemy.bindparam("b_user_id"))
            )

        Dbase.conn.execute(q, vals)


def times_append(message: types.Message):
    today = datetime.today().replace(microsecond=0)
    if not users_times.get(message.from_user.id):
        users_times[message.from_user.id] = [today]
    else:
        users_times[message.from_user.id].append(today)


def times_update():
    """
    Reset timer, user dicts and write to database
    """
    global timer
    UpdateTimes()
    timer = time()
    users_times.clear()


def dec_times_append(func):
    """
    Appends datetime.today to list of times for user_id
    when user_id send any text message
    """
    @wraps(func)
    def wrapper(message: types.Message):
        times_append(message)
        return func(message)

    return wrapper


def dec_times_update_timer(func):
    """
    Updates list of times in database
    for any user_id who send text messages
    every hour
    """

    @wraps(func)
    def wrapper(message: types.Message):
        if time() - timer >= 3600:
            print(users_times)
            times_update() if users_times else False
        return func(message)
    
    return wrapper


def dec_times_update_force(func):
    """
    Force update list of times in database
    for any user_id who send text messages
    """

    @wraps(func)
    def wrapper(message: types.Message):
        times_update() if users_times else False
        return func(message)

    return wrapper