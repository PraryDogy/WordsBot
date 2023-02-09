from . import (Counter, Dbase, Times, Words, bot, datetime,
               dec_times_update_force, dec_update_user, dec_words_update_force,
               get_nouns, json, sqlalchemy, types)

days = {
    0: "понедельник",
    1: "вторник",
    2: "среда",
    3: "четверг",
    4: "пятница",
    5: "суббота",
    6: "воскресенье"
    }

hours = {
    0: "часов",
    1: "час",
    **{i: "часа" for i in range(2, 5)},
    **{i: "часов" for i in range(5, 21)},
    21: "час",
    **{i: "часа" for i in range(22, 25)},
}


def user_words_get(message: types.Message, limit: int):

    q = (
        sqlalchemy.select(
            Words.word,
            Words.count
            )
        .filter(
            Words.user_id==message.from_user.id,
            Words.chat_id==message.chat.id
            )
        .order_by(-Words.count)
        .limit(limit)
        )
    return dict(Dbase.conn.execute(q).all())


def user_words_stat_get(message: types.Message):
    return (
        Dbase.conn.execute(
            sqlalchemy.select(
                Dbase.sq_count(Words.word),
                Dbase.sq_sum(Words.count)
                )
            .filter(
                Words.user_id == message.from_user.id,
                Words.chat_id == message.chat.id
                )
                ).all()
                )


def user_times_get(message: types.Message):
    return Dbase.conn.execute(
        sqlalchemy.select(Times.times_list)
        .filter(
            Times.user_id==message.from_user.id,
            Times.chat_id==message.chat.id
            )
            ).all()


def create_msg(message: types.Message, limit: int):
    load_times = user_times_get(message)

    if not load_times:
        return f"Нет данных. Пока что."

    deserialize = [json.loads(i[0]) for i in load_times]
    merge_times = [x for i in deserialize for x in i]
    str_to_datetime = [
        datetime.strptime(i, "%Y-%m-%d %H:%M:%S")
        for i in merge_times
        ]

    hours_count = Counter([i.hour for i in str_to_datetime])
    max_hour = max(hours_count, key=hours_count.get)

    weekdays_count = Counter([i.weekday() for i in str_to_datetime])
    find_max_weekday = max(weekdays_count, key=weekdays_count.get)
    max_weekday = days[find_max_weekday]

    messages_count = len(str_to_datetime)
    first_date = min(str_to_datetime).date()

    dates_count = Counter([i.date() for i in str_to_datetime])
    max_date = max(dates_count, key=dates_count.get)

    words_stats = user_words_stat_get(message)
    uniq_words, all_words = words_stats[0]
    
    msg_average = round(all_words/messages_count, 2)


    user_words = user_words_get(message, limit)

    user_nouns = {
        nn: user_words[nn]
        for nn in get_nouns(user_words.keys())
        }

    msg = (
        f"@{message.from_user.username}, ваша статистика:",
        f"Начало статистики: {first_date.strftime('%d %B %Y')}",
        f"Больше всего писал(a): {max_date.strftime('%d %B %Y')}",
        f"Cамый активный день: {max_weekday}",
        f"Самый активный час: {max_hour:02d} {hours[max_hour]}",
        f"Всего сообщений: {messages_count}",
        f"Всего слов: {all_words}",
        f"Словарный запас: {uniq_words}",
        f"Средняя длина сообщения: {msg_average}",

        "\nТоп 10 слов:",

        ", ".join([
            f"{x}: {y}"
            for x, y in tuple(user_words.items())[:10]
            ]),

        '\nТоп 10 существительных:',

        ", ".join([
            f'{x}: {y}'
            for x, y in tuple(user_nouns.items())[:10]
            ]),
            
            )

    return '\n'.join(msg)


@dec_update_user
@dec_words_update_force
@dec_times_update_force

async def send_msg(message: types.Message):

    await bot.send_message(
        message.chat.id,
        text=create_msg(message, 500)
        )