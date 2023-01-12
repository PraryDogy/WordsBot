import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy import Column, ForeignKey, Integer, Text

import cfg

class Dbase():
    """
    Checks database exists with DbChecker.

    *var conn: database connection
    *var base: declatative_base for models and actions
    """
    engine = sqlalchemy.create_engine(
        'sqlite:///' + 'test_db.db',
        connect_args={'check_same_thread':False,},
        echo= False
        )
    conn = engine.connect()
    base = sqlalchemy.ext.declarative.declarative_base()
    sq_sum = sqlalchemy.sql.expression.func.sum
    sq_count = sqlalchemy.sql.expression.func.count
    sq_lower = sqlalchemy.func.lower


class Words(Dbase.base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(Text)
    count = Column(Integer)
    user_id = Column(Integer)
    chat_id = Column(Integer)


# create_tables = Dbase.base.metadata.create_all(Dbase.conn)

from datetime import datetime
from collections import Counter


def db_words_record(msg_usr_id, msg_chat_id, words_list):
    """
    Gets all user's words with all chats ids  from database
    If word from input words list not in database words list - adds new row
    If word in database words list but has other chat id - adds new row
    If word in database words list and has the same chat id - updates word counter
    * `words_list`: list of words
    """
    for i in words_list:
        query = sqlalchemy.select(Words.id, Words.word, Words.count)\
            .where(Words.user_id==msg_usr_id, Words.chat_id==msg_chat_id)
        db_data = Dbase.conn.execute(query).all()

    db_words = [i[1] for i in db_data]
    new_words = Counter([i for i in words_list if i not in db_words])

    for w, c in new_words.items():
        vals = {'word': w, 'count': c, 'user_id': msg_usr_id, 'chat_id': msg_chat_id}
        q = sqlalchemy.insert(Words).values(vals)
        Dbase.conn.execute(q)

    old_words = [(x, y, z) for x, y, z in db_data if y in words_list]

    for x, y, z in old_words:
        vals = {'count': z + len([i for i in words_list if i == y])}
        q = sqlalchemy.update(Words).where(Words.id==x).values(vals)
        Dbase.conn.execute(q)

import random

msg = 'шла саша по шоссе и сосала сушку'
db_words_record(182, 864, msg.split())
