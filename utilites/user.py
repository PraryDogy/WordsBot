from . import Dbase, Users, datetime, sqlalchemy, timedelta, types, wraps, bot

__all__ = (
    "User",
    "dec_update_user",
    "create_mention",
    )


class User:
    def __init__(self, message: types.Message):
        self.user_id = message.from_user.id
        self.today = datetime.today().replace(microsecond=0)

    def user_check(self):
        q = (
            sqlalchemy.select(Users)
            .filter(Users.user_id == self.user_id)
            )
        try:
            return dict(Dbase.conn.execute(q).first())
        except TypeError:
            return False

    def create_db_user(self):
        new_user = {
                'user_id': self.user_id,
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

        user = User(message)

        if not user.user_check():
            user.create_db_user()

        return func(message)
    return wrapper


def create_mention(message: types.Message):
    """
    Creates mention based on user_id and first_name
    """
    return (
            f"[{str(message.from_user.first_name)}]"
            f"(tg://user?id={str(message.from_user.id)})"
            )


async def get_usernames(message: types.Message, id_list: list):
    """
    out: {user_id: username, ...}
    """
    # members = [
    #     await bot.get_chat_member(
    #         chat_id = message.chat.id,
    #         user_id = i
    #         )
    #     for i in id_list
    #     ]

    members = []
    for i in id_list:
        try:
            members.append(
                await bot.get_chat_member(
                    chat_id = message.chat.id,
                    user_id = i
                    )
                )
        except Exception:
            pass

    return {i.user.id: i.user.first_name for i in members}