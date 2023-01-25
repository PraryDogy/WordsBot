import re
from datetime import datetime, timedelta

import clipboard
import sqlalchemy

from database import *
from dicts import *
from text_analyser import *
from aiogram import Bot


def db_user_record(msg_user_id: int, msg_username: str):
    """
    Checks database `Users` table for user by `user_id` from message.
    Creates new record if user not exists.
    Updates username of exists user if it was changed.
    """
    get_user = sqlalchemy.select(
        Users.user_id, Users.user_name).filter(Users.user_id == msg_user_id)
    db_user = Dbase.conn.execute(get_user).first()

    if not msg_username:
        msg_username = 'Без имени'

    if not db_user:
        vals = {
            'user_id': msg_user_id,
            'user_name': msg_username,
            'user_time': datetime.today().replace(microsecond=0) - timedelta(days=1)}
        new_user = sqlalchemy.insert(Users).values(vals)
        Dbase.conn.execute(new_user)

    elif msg_username != db_user[1]:
        vals = {'user_name': msg_username}
        update_user = sqlalchemy.update(Users)\
            .where(Users.user_id==msg_user_id).values(vals)
        Dbase.conn.execute(update_user)


def get_user_time(user_id, today):
    """
    Returns time from database by user_id in datetime format.
    """
    get_time = sqlalchemy.select(Users.user_time)\
        .where(Users.user_id==user_id)
    res = Dbase.conn.execute(get_time).first()
    if not res:
        return today
    return datetime.strptime(res[0], '%Y-%m-%d %H:%M:%S')


def update_user_time(need_update, today, user_id):
    if need_update:
        vals = {'user_time': str(today)}
        q = sqlalchemy.update(Users).filter(Users.user_id==user_id)\
            .values(vals)
        Dbase.conn.execute(q)


def get_file_id(message):
    reg = r'"file_id": "\S*"'
    res = re.findall(reg, str(message))
    file_id = res[-1].split(' ')[-1].strip('"')
    clipboard.copy(file_id)
    return file_id


def khalisi_politic(message: str):
    for rus, eng in ru_eng_abc.items():
        if eng in message:
            message = message.replace(eng, rus)

    words_list = message.lower().split()
    for msg_word in words_list:
        for p_word in politic_words:
            if p_word in msg_word:
                return True
    return False


async def khalisi(message: str, bot: Bot):
    if khalisi_politic(message.text):
        if len(message.text) <= 1024:
            print(1)
            await bot.send_photo(
                message.chat.id,
                photo='AgACAgIAAxkBAAIBV2POwpjYW1G09NsaIn9UWcVfTAVMAAL2wjEbcDFwSvLDY7j9liSpAQADAgADeAADLQQ',
                reply_to_message_id=message.message_id,
                caption=khalisi_convert(message.text)
                )
        else:
            await bot.send_message(
                message.chat.id,
                reply_to_message_id=message.message_id,
                text='Слишком длинное сообщение для госпожи Кхалиси'
                )

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
            await bot.send_message(
                message.chat.id,
                reply_to_message_id=message.message_id,
                text='Выберите сообщение, которое хотите отправить Кхалиси'
            )