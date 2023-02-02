from time import time

from text_analyser import (get_nouns, morph, words_find, words_normalize,
                           words_stopwords)

from .handler_utils import (chat_words_get, db_sim_words, db_word_count,
                            db_word_people, user_get_words)
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
    def wrapper(*args):
        words_post() if users_words else False
        return func(*args)
    return wrapper


def msg_catch_words(user_id: int, chat_id: int, message: str):

    words = words_find(message.split())
    words = words_normalize(words)
    words = words_stopwords(words)

    if not users_words.get((user_id, chat_id)):
        users_words[(user_id, chat_id)] = words
    else:
        users_words[(user_id, chat_id)].extend(words)

    if time() - start >= 3600:
        words_post()


@dec_words_post
def user_words_top(chat_id: int, user: dict, limit: int):

    words = user_get_words(
        user['user_id'], chat_id, limit)

    nouns = {
        nn: words[nn]
        for nn in get_nouns(words.keys())
        }

    msg = (
        f"@{user['user_name']}, ваш топ 10 слов:",
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
def chat_words_top(chat_id: int, user: dict, limit: int):

    chat_words = chat_words_get(chat_id, limit)

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
       f"@{user['user_name']}, топ 10 слов чата:",
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
def top_boltunov(chat_id: int, user: dict):
    top = UsersTop(chat_id).strings_list

    msg = (
        f"@{user['user_name']}, топ 10 пиздюшек.",
        "Имя, количество слов, процент уникальных:\n",
        '\n'.join(top)
        )

    return '\n'.join(msg)


@dec_words_post
def word_stat(msg_chat_id, args: str):
    if not args:
        return 'Пример команды /word_stat слово.'

    similars = set()
    word_variants = (i.word for i in morph.parse(args)[0].lexeme)

    for i in word_variants:
        similars.update(db_sim_words(msg_chat_id, i))

    if not similars:
        return 'Нет данных о таком слове.'

    count = db_word_count(msg_chat_id, similars)
    people = len(db_word_people(msg_chat_id, similars))

    msg_list = []
    msg_list.append(f'Статистика слова {args}.')

    similar_words = ", ".join(sorted(similars))

    if similar_words:
        msg_list.append(f'Похожие слова: {similar_words}.')

    msg_list.append(f'Было сказано: {count} раз.')
    msg_list.append(f'Произносило: {people} человек.')

    return '\n'.join(msg_list)
