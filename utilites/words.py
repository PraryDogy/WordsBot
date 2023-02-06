import itertools
from collections import Counter
from functools import wraps
from time import time

import sqlalchemy
from aiogram import types

from database import Dbase, Words

from .main import sql_unions

words_timer: time = time()
users_words: dict = {}


class WordsWriter:
    def __init__(self):
        db_count = self.db_words_count(self.db_words_get())
        msg_count = self.msg_words_count()
        words = self.words_filter(db_count, msg_count)
        words = self.words_cleaner(words["old_words"], words["new_words"])

        if words['old_words']:
            self.db_update(words['old_words'])

        if words['new_words']:
            self.db_insert(words["new_words"])

    def db_words_get(self):
        """
        returns: `list`( `dict`(user_id, chat_id, word, count) )
        """
        queries = [
            sqlalchemy.select(
                Words.user_id, Words.chat_id, Words.word, Words.count
                )
            .filter(
                Words.user_id == user_id, Words.chat_id == chat_id,
                Words.word == w
                )
            for (user_id, chat_id), words in users_words.items()
            for w in set(words)
            ]

        return sql_unions(queries)

    def db_words_count(self, db_words):
        """
        *input: `list`(`dict`(user_id, chat_id, word, count))
        *returns: `dict`( (user_id, chat_id): `dict`(word: count) )
        """
        db_count = {
            (i["user_id"], i["chat_id"]): {}
            for i in db_words
            }

        for i in db_words:
            db_count[(i["user_id"], i["chat_id"])].update({i["word"]: i["count"]})

        return db_count

    def msg_words_count(self):
        """
        *returns: `dict`( (user_id, chat_id): `dict`(word: count) )
        """
        return {
            k: dict(Counter(v))
            for k, v in users_words.items()
            }

    def words_filter(self, db_words: dict, msg_words: dict):
        """
        * db_words_count: `dict`( (user_id, chat_id): `dict`(word: count) )
        * msg_words_count: `dict`( (user_id, chat_id): `dict`(word: count) )

        * returns: `dict` of dicts (old_words, new_words, new_users)
        * dicts items structure: (user_id, chat_id): `dict`(word: count)
        """

        old_words = {}
        new_words = {}

        for user, words in msg_words.items():

            if not db_words.get(user):
                new_words[user] = words
            else:
                old_words[user] = {}
                new_words[user] = {}

                for word, count in words.items():
                    try:
                        old_words[user][word] = db_words[user][word] + count
                    except KeyError:
                        new_words[user][word] = count
        
        return {"old_words": old_words, "new_words": new_words}

    def words_cleaner(self, old_words: dict, new_words: dict):
        clean_old = {
            user: words
            for user, words in old_words.items()
            if words
            }
        clean_new = {
            user: words
            for user, words in new_words.items()
            if words
            }
        
        return {"old_words": clean_old, "new_words": clean_new}

    def db_update(self, old_words: dict):
        vals = [
            {
            "b_user_id": user_id, "b_chat_id": chat_id,
            "b_word": word, "b_count": count
            }
            for (user_id, chat_id), words in old_words.items()
            for word, count in words.items()
            ]

        q = (
            sqlalchemy.update(Words)
            .values({'count': sqlalchemy.bindparam("b_count")})
            .where(
                Words.user_id==sqlalchemy.bindparam("b_user_id"),
                Words.chat_id==sqlalchemy.bindparam("b_chat_id"),
                Words.word==sqlalchemy.bindparam("b_word")
                )
                )

        Dbase.conn.execute(q, vals)

    def db_insert(self, new_words: dict):
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


def update_db_words():
    global words_timer
    WordsWriter()
    words_timer = time()
    users_words.clear()


def dec_update_db_words(func):

    @wraps(func)
    def wrapper(message: types.message):
        update_db_words() if users_words else False
        return func(message)

    return wrapper