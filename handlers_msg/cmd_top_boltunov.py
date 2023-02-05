from aiogram import types

from bot_config import bot
from database import Dbase, Users, Words, sqlalchemy
from utilites import dec_update_db_words, dec_update_user

class UsersTop:
    def __init__(self, chat_id):
        self.chat_id = chat_id

        users_ids = self.__load_users_ids()
        word_stats = self.__load_stat(users_ids)
        word_stats.sort(key=lambda x: x[1], reverse=1)

        self.strings_list = self.__list_stings(
            self.__load_users_names(users_ids),
            word_stats
            )

    def __load_users_ids(self):
        """
        returns: `list` of user_id filtered by chat_id
        """
        q = (
            sqlalchemy.select(Words.user_id)
            .distinct(Words.user_id)
            .filter(Words.chat_id==self.chat_id)
            )
        return [i[0] for i in Dbase.conn.execute(q).all()]

    def __load_users_names(self, users_ids):
        """
        returns: dict(user_id: user_name)
        """
        q = (
            sqlalchemy.select(Users.user_id, Users.user_name)
            .filter(Users.user_id.in_(users_ids))
            )
        return dict(Dbase.conn.execute(q).all())

    def __load_stat(self, id_list):
        """
        returns: tuple((user_id, words count sum, words count))
        """
        queries = [
            sqlalchemy.select(
                Words.user_id,
                Dbase.sq_sum(Words.count),
                Dbase.sq_count(Words.word))
            .filter(
                Words.user_id==i,
                Words.chat_id==self.chat_id)
            for i in id_list
            ]

        return (
            Dbase.conn.execute(sqlalchemy.union_all(*queries))
            .all()
            )

    def __list_stings(self, usernames, word_stats):
        return [
            (
                f"{usernames[user_id]}: "
                f"{words_count}, "
                f"{round((words_sum/words_count)*100)}%"
                )
            for user_id, words_count, words_sum in word_stats[:10]
            ]


def create_msg(message: types.Message):
    """
    user_id, user_name, chat_id
    """
    top = UsersTop(message.chat.id).strings_list

    msg = (
        f"@{message.from_user.username}, топ 10 пиздюшек.",
        "Имя, количество слов, процент уникальных:\n",
        '\n'.join(top)
        )

    return '\n'.join(msg)

@dec_update_user
@dec_update_db_words
async def send_msg(message: types.Message):
    msg = create_msg(message)
    await bot.send_message(chat_id=message.chat.id, text=msg)