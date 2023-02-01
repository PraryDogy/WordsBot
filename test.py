# from chatgpt_wrapper import ChatGPT


# def gpt():
#     bot = ChatGPT()
#     return bot.ask("Когда появился человек?")



import sqlalchemy

from test_db import Dbase, Users, Words


def db_insert(new_words: dict):
    vals = [
        {
        "b_user_id": user_id, "b_chat_id": chat_id,
        "b_word": word, "b_count": count
        }
        for (user_id, chat_id), words in new_words.items()
        for word, count in words.items()
        ]

    q = (
        sqlalchemy.insert(Words)
        .values({
            'word': sqlalchemy.bindparam("b_word"),
            'count': sqlalchemy.bindparam("b_count"),
            'user_id': sqlalchemy.bindparam("b_user_id"),
            'chat_id': sqlalchemy.bindparam("b_chat_id")
            })
            )

    Dbase.conn.execute(q, vals)


long_dict = {}
for i in range(10000):
    long_dict[(i, i)] = {"hui": 3}

# print(len(long_dict))

db_insert(long_dict)


