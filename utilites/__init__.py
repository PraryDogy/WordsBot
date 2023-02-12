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

from bot_config import DELETE_MESSAGES_TIMER, SQL_LIMIT, bot
from database import Dbase, Times, Users, Words
from dicts import khalisi_words, stop_words

from .del_messages import del_messages_append, del_msg_by_timer
from .text_analyser import (declension_n, get_lexeme, get_nouns,
                            khalisi_convert, words_find, words_normalize,
                            words_stopwords)
from .times import (dec_times_db_update_force, times_db_update_force,
                    times_dict_append)
from .user import User, create_mention, dec_update_user, get_usernames
from .words import dec_words_update_force, words_append, words_update_force


__all__ = (
    "create_mention",
    "del_messages_append",
    "del_msg_by_timer",
    "sql_unions",
    "get_nouns",
    "khalisi_convert",
    "get_lexeme",
    "declension_n",
    "words_find",
    "words_normalize",
    "words_stopwords",
    "times_dict_append",
    "dec_times_db_update_force",
    "times_db_update_force",
    "User",
    "dec_update_user",
    "dec_words_update_force",
    "words_append",
    "words_update_force",
    )