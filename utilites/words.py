from . import (Counter, Dbase, Words, datetime, sqlalchemy, types, words_find,
               words_normalize, words_stopwords, wraps)

__all__ = (
    "words_append",
    "words_update",
    "dec_words_update_force",
    )

LIMIT = 900
users_words: dict = {}
words_limit = []


class __UpdateWords:
    def __init__(self):
        self.year = datetime.today().year

        self.db_words = self.db_words_get()

        self.db_count = self.db_words_count()
        self.msg_count = self.msg_words_count()
        self.db_count_update()
        self.new_words_count = self.new_words()

        self.db_update() if self.db_count else False
        self.db_insert() if self.new_words_count else False

    def db_words_get(self):
        """
        returns: [ (user_id, chat_id, word, count) ]
        """
        queries = [
            sqlalchemy.select(
                Words.user_id,
                Words.chat_id,
                Words.word,
                Words.count
                )
            .filter(
                Words.user_id == user_id,
                Words.chat_id == chat_id,
                Words.word.in_(words),
                Words.year == self.year
                )
            for (user_id, chat_id), words in users_words.items()
            ]

        return Dbase.conn.execute(
            sqlalchemy.union_all(*queries)
            ).all()

    def db_words_count(self):
        """
        *returns: { (user_id, chat_id): {word: count} }
        """
        db_count = {
            (user_id, chat_id): {}
            for user_id, chat_id, _, _ in self.db_words
            }

        for user_id, chat_id, word, count in self.db_words:
            db_count[(user_id, chat_id)].update({word: count})

        return db_count

    def msg_words_count(self):
        """
        *returns: `dict`( (user_id, chat_id): `dict`(word: count) )
        """
        return {
            k: dict(Counter(v))
            for k, v in users_words.items()
            }

    def db_count_update(self):
        for user, words in self.db_count.items():
            for word, _ in words.items():
                self.db_count[user][word] += self.msg_count[user][word]

    def new_words(self):
        new_words = {}

        for user, words in self.msg_count.items():
            for word, count in words.items():
                try:
                    self.db_count[user]
                    self.db_count[user][word]
                except KeyError:
                    new_words[user] = {}

        for user, words in self.msg_count.items():
            for word, count in words.items():
                try:
                    self.db_count[user]
                    self.db_count[user][word]
                except KeyError:
                    new_words[user].update({word:count})

        return new_words

    def db_update(self):
        vals = [
            {
            "b_user_id": user_id,
            "b_chat_id": chat_id,
            "b_word": word,
            "b_count": count,
            "b_year": self.year
            }
            for (user_id, chat_id), words in self.db_count.items()
            for word, count in words.items()
            ]

        q = (
            sqlalchemy.update(Words)
            .values({'count': sqlalchemy.bindparam("b_count")})
            .filter(
                Words.user_id==sqlalchemy.bindparam("b_user_id"),
                Words.chat_id==sqlalchemy.bindparam("b_chat_id"),
                Words.word==sqlalchemy.bindparam("b_word"),
                Words.year==sqlalchemy.bindparam("b_year")
                )
                )

        Dbase.conn.execute(q, vals)

    def db_insert(self):
        vals = [
            {
            "b_user_id": user_id,
            "b_chat_id": chat_id,
            "b_word": word,
            "b_count": count,
            "b_year": self.year
            }
            for (user_id, chat_id), words in self.new_words_count.items()
            for word, count in words.items()
            ]

        q = (
            sqlalchemy.insert(Words)
            .values({
                'word': sqlalchemy.bindparam("b_word"),
                'count': sqlalchemy.bindparam("b_count"),
                'user_id': sqlalchemy.bindparam("b_user_id"),
                'chat_id': sqlalchemy.bindparam("b_chat_id"),
                'year': sqlalchemy.bindparam("b_year")
                })
                )

        Dbase.conn.execute(q, vals)


def __words_update():
    __UpdateWords()
    users_words.clear()
    words_limit.clear()


def words_append(message: types.Message):
    """
    Appends words from this message for this user_id and chat_id
    to users dict
    """
    words = words_find(message.text.split())
    words = words_normalize(words)
    words = list(words_stopwords(words))

    words_limit.extend(words)

    if not users_words.get((message.from_user.id, message.chat.id)):
        users_words[(message.from_user.id, message.chat.id)] = words
    else:
        users_words[(message.from_user.id, message.chat.id)].extend(words)


def words_update():
    """
    Updates words database if > 900.
    Return true if > 900 words, else False
    """
    if len(words_limit) >= LIMIT:
        __words_update()
        return True
    return False


def dec_words_update_force(func):
    """
    Force update database words
    """
    @wraps(func)
    def wrapper(message: types.message):
        __words_update() if users_words else False
        return func(message)

    return wrapper
