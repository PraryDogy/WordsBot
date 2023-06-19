from . import (Dbase, Words, bot, dec_times_db_update_force, dec_update_user,
               dec_words_update_force, get_lexeme, sqlalchemy, types)
import links

__all__ = (
    "send_msg"
    )


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
    first_word = message.reply_to_message.text.split()[0]

    similars = set()
    word_variants = (i.word for i in get_lexeme(first_word))

    for i in word_variants:
        similars.update(db_sim_words(message.chat.id, i))

    if not similars:
        return 'Нет данных о таком слове.'

    count = db_word_count(message.chat.id, similars)
    people = len(db_word_people(message.chat.id, similars))

    msg_list = []
    msg_list.append(f"Статистика слова \"{first_word}\".")

    similar_words = ", ".join(sorted(similars))

    if similar_words:
        msg_list.append(f'Похожие слова: {similar_words}.')

    msg_list.append(f'Было сказано: {count} раз.')
    msg_list.append(f'Произносило: {people} человек.')

    return '\n'.join(msg_list)

@dec_update_user
@dec_words_update_force
@dec_times_db_update_force
async def send_msg(message: types.Message):
    try:

        message.reply_to_message.text
        msg = create_msg(message)
        await bot.send_message(message.chat.id, text=msg)

    except Exception as e:
        await bot.send_photo(
            chat_id = message.chat.id,
            photo=links.wordstat_err,
            caption = "Пришлите одно слово с реплаем.",
            reply_to_message_id = message.message_id
            )

