from . import (Counter, Dbase, Times, Users, Words, bot, datetime,
               dec_times_update_force, dec_update_user, dec_words_update_force,
               json, sqlalchemy, types)

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


def create_msg(message: types.Message):

    q = (
        sqlalchemy.select(Times.times_list)
        .filter(
            Times.user_id==message.from_user.id,
            Times.chat_id==message.chat.id
            )
        )
    res = Dbase.conn.execute(q).first()

    if not res:
        return f"Нет данных. Пока что."

    res = json.loads(res[0])
    timed = [
        datetime.strptime(i, "%Y-%m-%d %H:%M:%S")
        for i in res
        ]

    hours_count = Counter([i.hour for i in timed])
    max_hour = max(hours_count, key=hours_count.get)

    weekdays_count = Counter([i.weekday() for i in timed])
    max_weekday = max(weekdays_count, key=weekdays_count.get)
    max_weekday = days[max_weekday]

    messages_count = len(timed)
    first_date = min(timed).date()

    most_active = Counter([i.date() for i in timed])
    most_active: datetime = max(most_active, key=most_active.get)

    q = (
        sqlalchemy.select(Dbase.sq_count(Words.word))
        .filter(Words.user_id == message.from_user.id)
    )

    msg = (
        f"@{message.from_user.username}, ваша статистика:",
        f"Начало статистики: {first_date.strftime('%d %B %Y')}",
        f"Больше всего писал(a): {most_active.strftime('%d %B %Y')}",
        f"Cамый активный день: {max_weekday}",
        f"Пик активности в: {max_hour:02d} {hours[max_hour]}",
        f"Всего сообщений: {messages_count}",
        )

    return "\n".join(msg)


@dec_update_user
@dec_words_update_force
@dec_times_update_force
async def send_msg(message: types.Message):
    msg = create_msg(message)
    await bot.send_message(message.chat.id, text=msg)