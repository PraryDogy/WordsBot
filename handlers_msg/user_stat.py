from . import (Counter, Dbase, Times, Words, bot, create_mention, datetime,
               dec_times_db_update_force, dec_update_user,
               dec_words_update_force, declension_n, get_nouns, json,
               sqlalchemy, types)

days = {
    0: "понедельник",
    1: "вторник",
    2: "среда",
    3: "четверг",
    4: "пятница",
    5: "суббота",
    6: "воскресенье"
    }

def db_words_user(message: types.Message, limit: int):
    """
    out: {word: count, ...}
    """
    q = (
        sqlalchemy.select(Words.word, Words.count)
        .filter(
            Words.user_id==message.from_user.id,
            Words.chat_id==message.chat.id)
        .order_by(-Words.count)
        .limit(limit)
        )
    return dict(Dbase.conn.execute(q).all())


def db_words_user_count_sum(message: types.Message):
    """
    out: (count of user's words, sum of counts user's words)
    """
    return (
        Dbase.conn.execute(
            sqlalchemy.select(
                Dbase.sq_count(Words.word), Dbase.sq_sum(Words.count))
            .filter(
                Words.user_id == message.from_user.id,
                Words.chat_id == message.chat.id)
                ).all()
                )


def user_times_get(message: types.Message):
    """
    out: ["datetime", ...] for json.loads()
    """
    return Dbase.conn.execute(
        sqlalchemy.select(Times.times_list)
        .filter(
            Times.user_id == message.from_user.id,
            Times.chat_id == message.chat.id)
            ).first()


def create_msg(message: types.Message):
    datetimes_loaded = user_times_get(message)

    if not datetimes_loaded:
        return f"Нет данных. Пока что."

    datetimes = json.loads(datetimes_loaded[0])

    datetimes = [
        datetime.strptime(i, "%Y-%m-%d %H:%M:%S")
        for i in datetimes
        ]

    hours = [i.hour for i in datetimes]
    most_pop_hour = max(hours, key=hours.count)

    weekdays = [i.weekday() for i in datetimes]
    most_pop_weekday = max(weekdays, key=weekdays.count)

    datetimes_len = len(datetimes)
    first_datetime = min(datetimes).date()

    dates_count = Counter([i.date() for i in datetimes])
    max_date = max(dates_count, key=dates_count.get)

    words_count_sum = db_words_user_count_sum(message)
    words_sum, words_counts_sum = words_count_sum[0]

    msg_average_len = round(words_counts_sum/datetimes_len, 0)

    user_words = db_words_user(message, 500)

    user_nouns = {
        nn: user_words[nn]
        for nn in get_nouns(user_words.keys())
        }

    msg = (
        f"{ create_mention(message) }, ваша статистика c "
        f"{ first_datetime.strftime('%d %B %Y') }:",

        "• Самый активный день за все время: "
        f"{ max_date.strftime('%d %B %Y') }",

        f"• Cамый активный день недели: { days[most_pop_weekday] }",

        "• Самое активное время: "
        f"{ most_pop_hour } { declension_n('час', most_pop_hour) }"
        f"{ ' ночи' if most_pop_hour in [23, 0, 1, 2, 3, 4] else '' }",

        f"• Всего сообщений: { datetimes_len }",

        f"• Всего слов: { words_counts_sum }",

        "• Словарный запас: "
        f"{ words_sum } { declension_n('слово', words_sum) }",

        "• Средняя длина сообщения: "
        f"{ msg_average_len:.0f} { declension_n('слово', msg_average_len) }",

        "\nТоп 10 слов:",
        ", ".join([word for word in list(user_words)][:10]),

        "\nТоп 10 существительных:",
        ", ".join([word for word in list(user_nouns)][:10]),

        )

    return '\n'.join(msg)


@dec_update_user
@dec_words_update_force
@dec_times_db_update_force

async def send_msg(message: types.Message):

    await bot.send_message(
        message.chat.id,
        text=create_msg(message),
        parse_mode="MARKDOWN"
        )

