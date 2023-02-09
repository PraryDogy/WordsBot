import itertools
import json
import re
from collections import Counter
from datetime import datetime, timedelta
from functools import wraps
from time import time

import pymorphy2
import spacy
import sqlalchemy
from aiogram import types

from bot_config import bot, delete_msg_timer
from database import Dbase, Times, Users, Words
from dicts import khalisi_words, stop_words

from .del_messages import del_messages_timer, del_messages_append
from .text_analyser import (get_nouns, khalisi_convert, morph, words_find,
                            words_normalize, words_stopwords)
from .times import dec_times_db_update_force, times_dict_append, times_db_update_force
from .user import UserData, dec_update_user
from .words import dec_words_update_force, words_append, words_update

__all__ = (
    "del_messages_append",
    "del_messages_timer",
    "sql_unions",
    "get_nouns",
    "khalisi_convert",
    "morph",
    "words_find",
    "words_normalize",
    "words_stopwords",
    "times_dict_append",
    "dec_times_db_update_force",
    "UserData",
    "dec_update_user",
    "dec_words_update_force",
    "words_append",
    "words_update",
    )