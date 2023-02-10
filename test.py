
from datetime import datetime
from database import *
import sqlalchemy
from collections import Counter
import bot_config


msg_count = {
        (444, 444): {'new': 5, 'newnew': 7},
        (13212, -13212): {"мама":6}
    }

db_count = {
        (13212, -13212): {'мама': 3}
    }


def new_words():
    new_words = {}

    for user, words in msg_count.items():
        for word, count in words.items():
            try:
                db_count[user]
                db_count[user][word]
            except KeyError:
                new_words.setdefault(user, {}).update({word:count})

    return new_words


print(new_words())