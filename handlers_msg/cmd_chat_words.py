from . import (Dbase, Words, bot, dec_update_user, dec_words_update_force, get_nouns,
               sqlalchemy, types)

__all__ = (
    "send_msg"
    )


def chat_words_get(chat_id: int, limit: int):
    q = (
        sqlalchemy.select(Words.word, Words.count)
        .filter(Words.chat_id==chat_id)
        .order_by(-Words.count)
        .limit(limit)
        )
    return Dbase.conn.execute(q).fetchall()


def create_msg(message: types.Message, limit: int):
    chat_words = chat_words_get(message.chat.id, limit)

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
       f"@{message.from_user.username}, топ 10 слов чата:",
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


@dec_update_user
@dec_words_update_force
async def send_msg(message: types.Message):
    msg = create_msg(message, limit=500)
    await bot.send_message(chat_id=message.chat.id, text=msg)