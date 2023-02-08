from time import sleep

import clipboard
import sqlalchemy

import bot_config
from database import Dbase, Users, Words


def parse_urls():

    with open('_urls.txt', 'w') as file:
        pass

    paste = '1'
    counter = 0

    while 'google' not in paste:
        new_paste = clipboard.paste()

        if new_paste != paste:

            paste = new_paste

            with open('_urls.txt', 'a') as file:
                file.write(new_paste + '\n')

                counter += 1
                print(counter)
                print('write url')
        
        sleep(0.1)


import json
import locale
from collections import Counter
from datetime import datetime

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

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


def create_msg(message: str):

    q = (
        sqlalchemy.select(Users.times)
        .filter(Users.user_id==message)
        # .filter(Users.user_id==message.from_user.id)
        )
    res = Dbase.conn.execute(q).first()[0]
    res = json.loads(res)
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
        .filter(Words.user_id == message)
    )
    res = Dbase.conn.execute(q).first()[0]

    msg = (
        f"Начало статистики: {first_date.strftime('%d %B %Y')}",
        f"Больше всего писал(a): {most_active.strftime('%d %B %Y')}",
        f"Cамый активный день: {max_weekday}",
        f"Пик активности в: {max_hour:02d} {hours[max_hour]}",
        f"Всего сообщений: {messages_count}",
        f"Словарный запас: {res}"
    )

    return "\n".join(msg)
