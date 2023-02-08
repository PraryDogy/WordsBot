import json
import locale
import re
from collections import Counter
from datetime import datetime

import clipboard
import humanize
import sqlalchemy
from aiogram import types

from bot_config import bot
from database import Dbase, Times, Users, Words, sqlalchemy
from utilites import (dec_times_append, dec_times_update_force,
                      dec_times_update_timer, dec_update_user,
                      dec_words_update_force, get_nouns, khalisi_convert,
                      morph, words_append, words_update_timer)

from .cmd_chat_words import send_msg as chat_words_top
from .cmd_khalisi import send_msg as khalisi_msg
from .cmd_start import send_msg as start
from .cmd_top_boltunov import send_msg as top_boltunov
from .cmd_user_words import send_msg as user_words_top
from .cmd_word_stat import send_msg as word_stat
from .my_stat import send_msg as my_stat
from .on_exit import on_exit_fn as on_exit
from .photo_id import msg_file_id as get_file_id
from .words_catch import msg_catch_words

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


__all__ = (
    "my_stat",
    "on_exit",
    "chat_words_top",
    "khalisi_msg",
    "start",
    "top_boltunov",
    "user_words_top",
    "word_stat",
    "get_file_id",
    "msg_catch_words"
)