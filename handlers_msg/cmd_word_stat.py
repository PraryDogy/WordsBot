import sqlalchemy
from aiogram import types

from bot_config import bot
from database import Dbase, Words
from utilites import dec_update_db_words, dec_update_user, morph


def db_sim_words(msg_chat_id, input_word):
    q = sqlalchemy.select(Words.word)\
    .filter(Words.chat_id==msg_chat_id, Words.word.like('%'+input_word+'%'))
    return set(i[0] for i in Dbase.conn.execute(q).all())


def db_word_count(msg_chat_id, words_list):
    q = sqlalchemy.select(Dbase.sq_sum(Words.count))\
        .filter(Words.chat_id==msg_chat_id, Words.word.in_(words_list))
    return Dbase.conn.execute(q).first()[0]


def db_word_people(msg_chat_id, words_list):
    q = sqlalchemy.select(Words.user_id)\
        .filter(Words.chat_id==msg_chat_id, Words.word.in_(words_list))

    return set(i[0] for i in Dbase.conn.execute(q).all())


def create_msg(message: types.Message):
    """
    word, user_id, user_name, chat_id
    """

    if not message.get_args():
        return 'Пример команды /word_stat слово.'

    similars = set()
    word_variants = (i.word for i in morph.parse(message.get_args())[0].lexeme)

    for i in word_variants:
        similars.update(db_sim_words(message.chat.id, i))

    if not similars:
        return 'Нет данных о таком слове.'

    count = db_word_count(message.chat.id, similars)
    people = len(db_word_people(message.chat.id, similars))

    msg_list = []
    msg_list.append(f'Статистика слова {message.get_args()}.')

    similar_words = ", ".join(sorted(similars))

    if similar_words:
        msg_list.append(f'Похожие слова: {similar_words}.')

    msg_list.append(f'Было сказано: {count} раз.')
    msg_list.append(f'Произносило: {people} человек.')

    return '\n'.join(msg_list)

@dec_update_user
@dec_update_db_words
async def send_msg(message: types.Message):
    msg = create_msg(message)
    await bot.send_message(message.chat.id, text=msg)
