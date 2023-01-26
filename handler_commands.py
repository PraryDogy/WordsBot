from time import time

import sqlalchemy

from database import *
from handler_utils import *
from text_analyser import *

start = time()
users_words_dict = {}

def users_words_write():
    global start

    if not users_words_dict:
        return

    for k, v in users_words_dict.items():
        db_words_record(k, v)
    
    start = time()
    users_words_dict.clear()


def catch_words(user_id: int, chat_id: int, message: str):
    words = words_stopwords(
        words_normalize(
            words_find(message.split())
            ))

    if not users_words_dict.get((user_id, chat_id)):
        users_words_dict[(user_id, chat_id)] = words
    else:
        users_words_dict[(user_id, chat_id)].extend(words)

    if time() - start >= 180:
        users_words_write()


def user_words_top(chat_id: int, user: dict, limit: int):
    users_words_write()

    words = user_get_words(user['user_id'], chat_id, limit)
    nouns = {nn: words[nn] for nn in get_nouns(words.keys())}

    msg = [
        f"@{user['user_name']}, ваш топ 10 слов:",
        *[(f"{x}: {y}") for x, y in tuple(words.items())[:10]],
        '\nТоп 10 существительных:',
        *[(f'{x}: {y}') for x, y in tuple(nouns.items())[:10]]
        ]

    return '\n'.join(msg)


def chat_words_top(chat_id: int, user: dict, limit: int):
    users_words_write()

    chat_words = chat_words_get(chat_id, limit)

    words_count = {}
    for word, count in chat_words:
            words_count[word] = words_count.get(word, 0) + count

    nouns_count = {nn: words_count[nn] for nn in get_nouns(words_count.keys())}

    words_top = sorted(words_count.items(), key = lambda x: x[1], reverse=1)[:10]
    nouns_top = sorted(nouns_count.items(), key = lambda x: x[1], reverse=1)[:10]

    msg = [
       f"@{user['user_name']}, топ 10 слов чата:",
        *[(f"{x}: {y}") for x, y in words_top],
        "\nТоп 10 существительных чата:",
        *[(f"{x}: {y}") for x, y in nouns_top]
        ]

    return '\n'.join(msg)


def top_boltunov(msg_chat_id: int, user: dict):
    users_words_write()
    user_words = []

    for user_id, user_name in db_all_usernames_get():

        q = (
            sqlalchemy.select(
                Dbase.sq_sum(Words.count),
                Dbase.sq_count(Words.word))
            .filter(
                Words.user_id==user_id,
                Words.chat_id==msg_chat_id)
                )
        all_words_c, uniq_words_c = Dbase.conn.execute(q).first()

        uniq = int(100*(uniq_words_c/all_words_c)) if uniq_words_c else False
        user_words.append((user_name, all_words_c, uniq)) if all_words_c else False

    user_words = sorted(user_words, key=lambda i: i[1], reverse=1)[:10]

    msg = [
        f"@{user['user_name']}, топ 10 пиздюшек.",
        "Имя, количество слов, процент уникальных:\n",
        *[f"{name}: {words}, {perc}%" for name, words, perc in user_words]
        ]

    return '\n'.join(msg)


def word_stat(msg_chat_id, args: str):
    users_words_write()

    if not args:
        return 'Пример команды /word_stat слово.'

    similars = set()
    word_variants = [i.word for i in morph.parse(args)[0].lexeme]

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
