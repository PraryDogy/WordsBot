from . import (Counter, Dbase, Times, Users, Words, bot, datetime,
               dec_times_db_update_force, dec_update_user, dec_words_update_force,
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


class UsersTop:
    def __init__(self, message: types.Message):
        self.chat_id = message.chat.id

        users_ids = self.__load_users_ids()
        word_stats = self.__load_stat(users_ids)
        word_stats.sort(key=lambda x: x[1], reverse=1)

        self.user_names = self.__load_users_names(users_ids)

        self.strings_list = self.__list_stings(
            self.user_names,
            word_stats
            )

    def __load_users_ids(self):
        """
        returns: `list` of user_id filtered by chat_id
        """
        q = (
            sqlalchemy.select(Words.user_id)
            .distinct(Words.user_id)
            .filter(Words.chat_id==self.chat_id)
            )
        return [i[0] for i in Dbase.conn.execute(q).all()]

    def __load_users_names(self, users_ids):
        """
        returns: dict(user_id: user_name)
        """
        q = (
            sqlalchemy.select(Users.user_id, Users.user_name)
            .filter(Users.user_id.in_(users_ids))
            )
        return dict(Dbase.conn.execute(q).all())

    def __load_stat(self, id_list):
        """
        returns: tuple((user_id, words count sum, words count))
        """
        queries = [
            sqlalchemy.select(
                Words.user_id,
                Dbase.sq_sum(Words.count),
                Dbase.sq_count(Words.word))
            .filter(
                Words.user_id==i,
                Words.chat_id==self.chat_id)
            for i in id_list
            ]

        return (
            Dbase.conn.execute(sqlalchemy.union_all(*queries))
            .all()
            )

    def __list_stings(self, usernames, word_stats):
        return [
            (
                f"{usernames[user_id]}: "
                f"{words_count}, "
                f"{round((words_sum/words_count)*100)}%"
                )
            for user_id, words_count, words_sum in word_stats[:10]
            ]


def chat_words_get(message: types.Message, limit: int):
    q = (
        sqlalchemy.select(
            Words.word,
            Words.count
            )
        .filter(
            Words.chat_id==message.chat.id
            )
        .order_by(-Words.count)
        .limit(limit)
        )
    return Dbase.conn.execute(q).all()


def chat_times_get(message: types.Message):
    return Dbase.conn.execute(
        sqlalchemy.select(
            Times.user_id,
            Times.times_list
            )
        .filter(
            Times.chat_id==message.chat.id
            )
            ).all()


def create_msg(message: types.Message, limit: int):
    load_times = chat_times_get(message)

    if not load_times:
        return f"Нет данных. Пока что."

    deserialized = [
        (user_id, json.loads(times_list))
        for user_id, times_list in load_times
        ]

    merged_times = [
        x
        for user_id, times_list in deserialized
        for x in times_list
        ]

    str_to_datetime = [
        datetime.strptime(i, "%Y-%m-%d %H:%M:%S")
        for i in merged_times
        ]

    hours_count = Counter([i.hour for i in str_to_datetime])
    max_hour = max(hours_count, key=hours_count.get)

    weekdays_count = Counter([i.weekday() for i in str_to_datetime])
    find_max_weekday = max(weekdays_count, key=weekdays_count.get)
    max_weekday = days[find_max_weekday]

    first_date = min(str_to_datetime).date()

    dates_count = Counter([i.date() for i in str_to_datetime])
    max_date = max(dates_count, key=dates_count.get)

    chat_words = chat_words_get(message, limit)

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

    users_data = UsersTop(message)
    top = users_data.strings_list
    usernames = users_data.user_names

    messages_top = [
        (usernames[user_id], len(times_list))
        for user_id, times_list in deserialized
        ]

    msg = (
        f"@{message.from_user.username}, статистика чата:",
        f"Начало статистики: {first_date.strftime('%d %B %Y')}",
        f"Больше всего сообщений было: {max_date.strftime('%d %B %Y')}",
        f"Cамый активный день: {max_weekday}",
        f"Самый активный час: {max_hour:02d} {hours[max_hour]}",

        "\nТоп 10 слов:",

        ", ".join([
            f"{x}: {y}"
            for x, y in words_top[:10]
            ]),

        '\nТоп 10 существительных:',

        ", ".join([
            f'{x}: {y}'
            for x, y in nouns_top[:10]
            ]),

        "\nТоп 10 по словам (имя: кол-во слов, коэф. уникальных):",
        '\n'.join(top),

        "\nТоп 10 по сообщениям:",
        "\n".join([
            f"{x}: {y}"
            for x, y in messages_top[:10]
            ]),
        )

    return '\n'.join(msg)


@dec_update_user
@dec_words_update_force
@dec_times_db_update_force

async def send_msg(message: types.Message):

    await bot.send_message(
        message.chat.id,
        text=create_msg(message, 500)
        )