import re
from datetime import datetime, timedelta

import clipboard
import sqlalchemy

from database import *
from dicts import *
from text_analyser import *
from aiogram import Bot


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
            'user_time': datetime.today() - timedelta(days=1)
            }
    q = (sqlalchemy.insert(Users).values(new_user))
    Dbase.conn.execute(q)
    return new_user


def user_update_time(user_id: int, today: datetime):
    q = (
        sqlalchemy.update(Users)
        .filter(Users.user_id==user_id)
        .values({'user_time': today})
        )
    Dbase.conn.execute(q)


def user_actions(user_id: int, user_name: str):
    user = user_get(user_id)
    if not user:
        return user_create(user_id, user_name)
    else:
        user_update_name(user, user_name)
    return user


def get_file_id(message):
    reg = r'"file_id": "\S*"'
    res = re.findall(reg, str(message))
    file_id = res[-1].split(' ')[-1].strip('"')
    clipboard.copy(file_id)
    return file_id


async def khalisi(message: str, bot: Bot):
    if '@prariewords_bot' in message.text:
        try:
            khalisi_msg = khalisi_convert(message.reply_to_message.text)
            msg_reply_id = message.reply_to_message.message_id
            if len(message.reply_to_message.text) <= 1024:
                await bot.send_photo(
                    message.chat.id,
                    photo='AgACAgIAAxkBAAIBV2POwpjYW1G09NsaIn9UWcVfTAVMAAL2wjEbcDFwSvLDY7j9liSpAQADAgADeAADLQQ',
                    reply_to_message_id=msg_reply_id,
                    caption=khalisi_msg
                    )
            else:
                await bot.send_message(
                    message.chat.id,
                    reply_to_message_id=message.message_id,
                    text='Слишком длинное сообщение для госпожи Кхалиси'
                    )
        except AttributeError:
            pass
