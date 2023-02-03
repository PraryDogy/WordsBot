from functools import wraps
from time import time

from text_analyser import (get_nouns, morph, words_find, words_normalize,
                           words_stopwords)
from utils import UserData

from .handler_utils import (chat_words_get, db_sim_words, db_word_count,
                            db_word_people, user_words_get)
from .users_top import UsersTop
from .words_writer import WordsWriter

start = time()
users_words = {}


def words_post():
    global start
    WordsWriter(users_words)
    start = time()
    users_words.clear()


def dec_words_post(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        words_post() if users_words else False
        return func(*args, **kwargs)

    return wrapper


def dec_user_data(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        user = UserData(
            user_id=kwargs["user_id"],
            user_name=kwargs["user_name"]
            ).user_data_get()
        kwargs.update(user)
        return func(*args, **kwargs)

    return wrapper


@dec_user_data
def msg_catch_words(*args, **kwargs):
    """
    user_id, user_name, chat_id, message
    """
    words = words_find(kwargs["message"].split())
    words = words_normalize(words)
    words = words_stopwords(words)

    if not users_words.get((kwargs["user_id"], kwargs["chat_id"])):
        users_words[(kwargs["user_id"], kwargs["chat_id"])] = words
    else:
        users_words[(kwargs["user_id"], kwargs["chat_id"])].extend(words)

    if time() - start >= 3600:
        words_post()


@dec_words_post
@dec_user_data
def user_words_top(*args, **kwargs):
    """
    user_id, user_name, chat_id, limit
    limit: how many words load from database to create top words,
    500 recomended.
    """

    words = user_words_get(
        kwargs["user_id"], kwargs["chat_id"], kwargs["limit"])

    nouns = {
        nn: words[nn]
        for nn in get_nouns(words.keys())
        }

    msg = (
        f"@{kwargs['user_name']}, ваш топ 10 слов:",
        *[
            f"{x}: {y}"
            for x, y in tuple(words.items())[:10]
            ],
        '\nТоп 10 существительных:',
        *[
            f'{x}: {y}'
            for x, y in tuple(nouns.items())[:10]
            ],
            )

    return '\n'.join(msg)


@dec_words_post
@dec_user_data
def chat_words_top(*args, **kwargs):
    """
    user_id, user_name, chat_id, limit
    limit: how many words load from database to create top words,
    500 recomended.
    """
    chat_words = chat_words_get(kwargs["chat_id"], kwargs["limit"])

    words_count = {}
    for word, count in chat_words:
            words_count[word] = words_count.get(word, 0) + count

    nouns_count = {
        nn: words_count[nn]
        for nn in get_nouns(words_count.keys())
        }

    words_top = sorted(
        words_count.items(),
        key = lambda x: x[1],
        reverse=1
        )[:10]

    nouns_top = sorted(
        nouns_count.items(),
        key = lambda x: x[1],
        reverse=1
        )[:10]

    msg = (
       f"@{kwargs['user_name']}, топ 10 слов чата:",
        *[
            f"{x}: {y}"
            for x, y in words_top
            ],
        "\nТоп 10 существительных чата:",
        *[
            f"{x}: {y}"
            for x, y in nouns_top
            ]
            )

    return '\n'.join(msg)


@dec_words_post
@dec_user_data
def top_boltunov(*args, **kwargs):
    """
    user_id, user_name, chat_id
    """
    top = UsersTop(kwargs["chat_id"]).strings_list

    msg = (
        f"@{kwargs['user_name']}, топ 10 пиздюшек.",
        "Имя, количество слов, процент уникальных:\n",
        '\n'.join(top)
        )

    return '\n'.join(msg)


@dec_words_post
@dec_user_data
def word_stat(*args, **kwargs):
    """
    word, user_id, user_name, chat_id
    """
    if not kwargs["word"]:
        return 'Пример команды /word_stat слово.'

    similars = set()
    word_variants = (i.word for i in morph.parse(kwargs["word"])[0].lexeme)

    for i in word_variants:
        similars.update(db_sim_words(kwargs["chat_id"], i))

    if not similars:
        return 'Нет данных о таком слове.'

    count = db_word_count(kwargs["chat_id"], similars)
    people = len(db_word_people(kwargs["chat_id"], similars))

    msg_list = []
    msg_list.append(f'Статистика слова {kwargs["word"]}.')

    similar_words = ", ".join(sorted(similars))

    if similar_words:
        msg_list.append(f'Похожие слова: {similar_words}.')

    msg_list.append(f'Было сказано: {count} раз.')
    msg_list.append(f'Произносило: {people} человек.')

    return '\n'.join(msg_list)
