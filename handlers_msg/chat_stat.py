from . import (Counter, Dbase, Times, Users, Words, bot, create_mention,
               datetime, dec_times_db_update_force, dec_update_user,
               dec_words_update_force, declension_n, defaultdict, get_nouns,
               get_usernames, json, sqlalchemy, types)

days = {
    0: "понедельник",
    1: "вторник",
    2: "среда",
    3: "четверг",
    4: "пятница",
    5: "суббота",
    6: "воскресенье"
    }


def load_chat_users_ids(message: types.Message):
    """
    out: (user_id, ...)
    """
    q = (
        sqlalchemy.select(Words.user_id)
        .distinct(Words.user_id)
        .filter(Words.chat_id==message.chat.id)
        )

    return [i[0] for i in Dbase.conn.execute(q).all()]


def datetimes_get(message: types.Message):
    """
    out: [ (user_id, json list datetimes), ... ]
    """
    return Dbase.conn.execute(
        sqlalchemy.select(
            Times.user_id,
            Times.times_list
            )
        .filter(
            Times.chat_id==message.chat.id
            )
            ).all()


def datetimes_convert(datetimes_list):
    """
    * in: [ (user_id, json list datetimes), ... ]
    * out: [(user_id, list of datetimes), ... ]
    """
    return [
        (
            user_id,
            [
                datetime.strptime(i, "%Y-%m-%d %H:%M:%S")
                for i in json.loads(times_list)
                ]
            )

        for user_id, times_list in datetimes_list
        
        ]


def datetimes_merge(db_times_list: list):
    """
    * in: [(user_id, list of datetimes), ... ]
    * out: [datetime, ...]
    """
    return [
        x
        for _, times_list in db_times_list
        for x in times_list
        ]


def most_popular_hour_find(datetimes_list: list) -> datetime.hour:
    hours_count = Counter([i.hour for i in datetimes_list])
    return max(hours_count, key=hours_count.get)


def most_popular_weekday_find(datetimes_list: list):
    weekdays_count = Counter([i.weekday() for i in datetimes_list])
    find_max_weekday = max(weekdays_count, key=weekdays_count.get)
    return days[find_max_weekday]


def most_popular_date_find(datetimes_list: list):
    dates_count = Counter([i.date() for i in datetimes_list])
    return max(dates_count, key=dates_count.get)


def first_date_find(datetimes_list: list):
    return min(datetimes_list).date()


def chat_words_get(message: types.Message):
    q = (
        sqlalchemy.select(
            Words.word,
            Words.count
            )
        .filter(
            Words.chat_id==message.chat.id
            )
        .order_by(-Words.count)
        .limit(500)
        )
    return Dbase.conn.execute(q).all()


def words_count(chat_words: list):
    """
    * in: [ (word, count), ... ]
    * out: {word: sum of counts for this word from all users, ...}
    """
    res = defaultdict(int)
    for word, count in chat_words:
        res[word] += count
    return res


def top_chat_words(words_counted: list):
    """
    * in: {word: count, ...}
    * out: sorted top 10 [ (word, count), ... ]
    """
    return sorted(
        words_counted.items(),
        key = lambda x: x[1],
        reverse=1
        )[:10]


def top_chat_nouns(words_counted: list):
    """
    * in: {word: count, ...}
    * out: sorted top 10 nouns [ (word, count), ... ]
    """
    nouns_count = {
        nn: words_counted[nn]
        for nn in get_nouns(words_counted.keys())
        }

    return sorted(
        nouns_count.items(),
        key = lambda x: x[1],
        reverse=1
        )[:10]


def load_users_words_sum(message: types.Message, users_ids: list):
    """
    out: sorted by words_sum [(user_id, words_sum), ...]
    """
    queries = [
        sqlalchemy.select(
            Words.user_id,
            Dbase.sq_sum(Words.count).label("max")
            )
        .filter(
            Words.user_id==i,
            Words.chat_id==message.chat.id)

        for i in users_ids
        ]

    return sorted(
        Dbase.conn.execute(sqlalchemy.union_all(*queries)).all(),
        key = lambda x: x[1],
        reverse=True
        )

def top_users_by_words_sum(usernames: dict, users_words: list):
    """
    * in usernames: {user_id: username, ...}
    * in datetimes_converted: [(user_id, list of datetimes), ...]
    * out top users by times count [(username, times count), ...]
    """
    messages_len = [
        (usernames[user_id], word_count)
        for user_id, word_count in users_words
        ]

    return sorted(
        messages_len,
        key = lambda x: x[1],
        reverse=1
        )[:10]


def top_users_by_msg_count(usernames: dict, datetimes_converted: list):
    """
    * in usernames: {user_id: username, ...}
    * in datetimes_converted: [(user_id, list of datetimes), ...]
    * out top users by times count [(username, times count), ...]
    """
    messages_len = [
        (usernames[user_id], len(times_list))
        for user_id, times_list in datetimes_converted
        ]

    return sorted(
        messages_len,
        key = lambda x: x[1],
        reverse=1
        )[:10]


async def create_msg(message: types.Message):
    chat_times = datetimes_get(message)

    if not chat_times:
        return "Нет данных. Пока что."

    datetimes_converted = datetimes_convert(chat_times)
    datetimes_merged = datetimes_merge(datetimes_converted)

    first_date: datetime = first_date_find(datetimes_merged)
    most_pop_hour: datetime = most_popular_hour_find(datetimes_merged)
    most_pop_date: datetime = most_popular_date_find(datetimes_merged)
    most_pop_weekday: datetime = most_popular_weekday_find(datetimes_merged)

    words_counted = words_count(chat_words_get(message))
    top_words = top_chat_words(words_counted)
    top_nns = top_chat_nouns(words_counted)

    users_ids = load_chat_users_ids(message)
    usernames = await get_usernames(message, users_ids)

    users_words = load_users_words_sum(message, users_ids)
    top_users_by_words = top_users_by_words_sum(usernames, users_words)

    top_users_by_msg = top_users_by_msg_count(usernames, datetimes_converted)

    msg = (
        f"{create_mention(message)}, статистика чата c "
        f"{first_date.strftime('%d %B %Y')}",

        "• Самый активный день за все время: "
        f"{most_pop_date.strftime('%d %B %Y')}",

        "• Cамый активный день недели: "
        f"{most_pop_weekday}",

        "• Самое активное время: "
        f"{most_pop_hour:.0f} {declension_n('час', most_pop_hour)}"
        f"{ ' ночи' if most_pop_hour in [23, 0, 1, 2, 3, 4] else '' }",

        "\nТоп 10 слов чата:",
        ", ".join([
            f"{word}" for word, _ in top_words
            ]),

        "\nТоп 10 существительных чата:",
        ", ".join([
            f"{noun}" for noun, _ in top_nns
            ]),

        "\nТоп 10 пользователей по кол-ву слов:",
        "\n".join([
            f"{x}: {y}" for x, y in top_users_by_words
            ]),

        "\nТоп 10 пользователей по кол-ву сообщений:",
        "\n".join([
            f"{x}: {y}" for x, y in top_users_by_msg
            ]),
        )

    return '\n'.join(msg)


@dec_update_user
@dec_words_update_force
@dec_times_db_update_force

async def send_msg(message: types.Message):

    await bot.send_message(
        message.chat.id,
        text= await create_msg(message),
        parse_mode="MARKDOWN"
        )


# надо удалить будет ;;;;;;;;;;;;;;;;;;;


@dec_update_user
@dec_words_update_force
@dec_times_db_update_force

async def temp_stat(message: types.Message):
    if message.from_user.id == 248208655:
        ''