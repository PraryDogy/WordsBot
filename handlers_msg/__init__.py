import json
import locale
import re
from collections import Counter
from datetime import datetime

import clipboard
import humanize
import sqlalchemy
from aiogram import types

from bot_config import bot, bot_name
from database import Dbase, Times, Users, Words, sqlalchemy
from utilites import (dec_times_append, dec_times_update_force,
                      dec_times_update_timer, dec_update_user,
                      dec_words_update_force, del_messages_timer,
                      for_delete_append, get_nouns, khalisi_convert, morph,
                      words_append, words_update_timer)

from .chat_stat import send_msg as chat_stat
from .info import send_msg as start
from .khalisi import send_msg as khalisi_msg
from .on_exit import on_exit_fn as on_exit
from .photo_id import msg_file_id as get_file_id
from .user_stat import send_msg as user_stat
from .word_stat import send_msg as word_stat
from .words_catch import msg_catch_words

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

__all__ = (
    "user_stat",
    "on_exit",
    "chat_stat",
    "khalisi_msg",
    "start",
    "top_boltunov",
    "user_words_top",
    "word_stat",
    "get_file_id",
    "msg_catch_words"
)