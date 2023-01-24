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


def users_words(user_id, chat_id, message: str):
    find_words = words_find(message.split())
    norm_words = words_normalize(find_words)
    res_words = words_stopwords(norm_words)

    if not users_words_dict.get(f'{user_id}/{chat_id}'):
        users_words_dict[f'{user_id}/{chat_id}'] = res_words
    else:
        users_words_dict[f'{user_id}/{chat_id}'].extend(res_words)

    if time() - start >= 180:
        users_words_write()


def user_words_top(msg_chat_id, msg_username, args: str):
    """
    Returns text with top 10 words of user in current chat.
    """
    users_words_write()

    if not args:
        user = db_user_get(msg_username)
    else:
        user = db_user_get(args.replace('@', ''))

    if not user:
        return 'Нет данных о пользователе'

    db_words = db_user_words_get(user[0], msg_chat_id, 500)
    db_nouns = get_nouns(db_words)[:10]

    msg = []
    if not args:
        msg.append(f'@{msg_username}, ваш топ 10 слов:')
    else:
        msg.append(f'@{msg_username}, топ 10 слов пользователя {user[1]}:')

    [msg.append(f'{x}: {y}') for x, y in db_words[:10]]
    msg.append('\nТоп 10 существительных:')
    [msg.append(f'{x}: {y}') for x, y in db_nouns]

    return '\n'.join(msg)


def chat_words_top(msg_chat_id, msg_username):
    """
    Telegram `/chat_words`. 
    Returns text with top 10 words in current chat.
    """
    users_words_write()

    words_db = db_chat_words_get(msg_chat_id, 500)

    words_sum = {}
    for letter, number in words_db:
            words_sum[letter] = words_sum.get(letter, 0) + number

    nouns_sum = get_nouns(words_sum.items())

    words_top = sorted(words_sum.items(), key = lambda x: x[1], reverse=1)[:10]
    nouns_top = sorted(nouns_sum, key = lambda x: x[1], reverse=1)[:10]

    msg = []
    msg.append(f'@{msg_username}, топ 10 слов чата:')
    [msg.append(f'{x}: {y}') for x, y in words_top]
    msg.append('\nТоп 10 существительных чата:')
    [msg.append(f'{x}: {y}') for x, y in nouns_top]

    return '\n'.join(msg)


def top_boltunov(msg_chat_id, msg_username):
    """
    Returns `text` with top 10 users by words count and top 10 users by unique
    words count.
    """
    users_words_write()
    user_words = []
    msg = []

    for db_user_id, db_user_name in db_all_usernames_get():

        q = sqlalchemy.select(
            Dbase.sq_sum(Words.count),
            Dbase.sq_count(Words.word))\
            .where(Words.user_id==db_user_id, Words.chat_id==msg_chat_id)
        all_words_c, uniq_words_c = Dbase.conn.execute(q).first()

        uniq = int(100*(uniq_words_c/all_words_c)) if uniq_words_c else False
        user_words.append((db_user_name, all_words_c, uniq)) if all_words_c else False

    user_words = sorted(user_words, key=lambda i: i[1], reverse=1)

    msg.append(f'@{msg_username}, топ 10 пиздюшек.')
    msg.append('Имя, количество слов, процент уникальных:\n')
    for name, words, perc in user_words[:10]:
        msg.append(f'{name}: {words}, {perc}%')

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
