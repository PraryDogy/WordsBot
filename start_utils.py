import re
from datetime import datetime, timedelta

import clipboard
import sqlalchemy

from bot_config import bot
from database import Dbase, Users
from text_analyser import khalisi_convert


def user_get(user_id: int):
    q = (
        sqlalchemy.select(Users)
        .filter(Users.user_id == user_id)
        )
    try:
        return dict(Dbase.conn.execute(q).first())
    except TypeError:
        return False


def user_update_name(user: dict, msg_user_name):
    if user['user_name'] != msg_user_name:
        q = (
            sqlalchemy.update(Users)
            .filter(Users.user_id==user['user_id'])
            .values({'user_name': msg_user_name})
            )
        return Dbase.conn.execute(q)
    return False


def user_create(user_id, user_name):
    new_user = {
            'user_id': user_id,
            'user_name': user_name,
            'user_time': datetime.today() - timedelta(days=1),
            'times': datetime.today().replace(microsecond=0)
            }

    Dbase.conn.execute(
        sqlalchemy.insert(Users)
        .values(new_user)
        )
    return new_user


def user_update_time(user_id: int, today: datetime):
    q = (
        sqlalchemy.update(Users)
        .filter(Users.user_id==user_id)
        .values({'user_time': today})
        )
    Dbase.conn.execute(q)


def user_data(user_id: int, user_name: str):
    user = user_get(user_id)
    if not user:
        return user_create(user_id, user_name)
    else:
        user_update_name(user, user_name)
    return user


def user_update_times(user_id: int):
    q = (
        sqlalchemy.select(Users.times)
        .filter(Users.user_id==user_id)
        )
    user_times: str = Dbase.conn.execute(q).first()[0]
    today = str(datetime.today().replace(microsecond=0))

    if not user_times:
        Dbase.conn.execute(
            sqlalchemy.update(Users)
            .filter(Users.user_id==user_id)
            .values(
                {"times": today}
                )
            )

    else:
        Dbase.conn.execute(
            sqlalchemy.update(Users)
            .filter(Users.user_id==user_id)
            .values(
                {"times": f"{user_times},{today}"}
                )
            )


def get_file_id(message):
    reg = r'"file_id": "\S*"'
    res = re.findall(reg, str(message))
    file_id = res[-1].split(' ')[-1].strip('"')
    clipboard.copy(file_id)
    return file_id


async def khalisi(message):
    try:
        msg: str = message.reply_to_message.text
    except AttributeError:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo="https://sun9-8.userapi.com/impg/o4h0YbL0OvfSp2_gpy7ZpQgeWAh2lBxMCZ-tQQ/yAnd91aXzvI.jpg?size=656x332&quality=95&sign=6b3582556c89078e48fc0f08f03a8347&type=album",
            caption="Вызовите Кхалиси с реплаем сообщения.",
            reply_to_message_id=message.message_id
            )
        return

    msg = ' '.join(
        khalisi_convert(
            msg.lower().split()
            )
            ).capitalize()

    await bot.send_photo(
        message.chat.id,
        photo="https://sun9-12.userapi.com/impg/oOGXM3AEHzVrTR77mtSmGE8HzRzb9_EN09z-0Q/OP2uh8gxsT4.jpg?size=460x300&quality=95&sign=ed7f5d437785ea571d4d95c5762c5c1f&type=album",
        reply_to_message_id=message.reply_to_message.message_id,
        caption=msg
        )
