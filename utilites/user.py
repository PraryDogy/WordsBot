from . import Dbase, Users, datetime, sqlalchemy, timedelta, types, wraps

__all__ = (
    "UserData",
    "dec_update_user",
    )


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
                }

        Dbase.conn.execute(
            sqlalchemy.insert(Users)
            .values(new_user)
            )

    def update_db_user_time(self):
        q = (
            sqlalchemy.update(Users)
            .filter(Users.user_id==self.user_id)
            .values({'user_time': self.today})
            )
        Dbase.conn.execute(q)

    def load_db_user_time(self):
        return (
            Dbase.conn.execute(
                sqlalchemy.select(Users.user_time)
                .filter(Users.user_id==self.user_id)
                ).first()[0]
                )


def dec_update_user(func):
    """
    Creates new database record for user if user not exists in database.
    Updates username if user changed username
    """

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


