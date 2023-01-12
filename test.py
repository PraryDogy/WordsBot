from collections import Counter

import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy import Column, ForeignKey, Integer, Text

import cfg
from text_analyser import normalize_word


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


class Users(Dbase.base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    user_name = Column(Text)
    last_time = Column(Text)


class Words(Dbase.base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(Text)
    count = Column(Integer)
    user_id = Column(Integer)
    chat_id = Column(Integer)

create_tables = Dbase.base.metadata.create_all(Dbase.conn)


def db_words_record(msg_usr_id, msg_chat_id, words_list):
    """
    Gets all user's words with all chats ids  from database
    If word from input words list not in database words list - adds new row
    If word in database words list but has other chat id - adds new row
    If word in database words list and has the same chat id - updates word counter
    * `words_list`: list of words
    """
    query = sqlalchemy.select(Words.id, Words.word, Words.count)\
        .where(Words.user_id==msg_usr_id, Words.chat_id==msg_chat_id)
    db_data = Dbase.conn.execute(query).all()

    db_words = [i[1] for i in db_data]
    norm_words = [normalize_word(i) for i in db_words]

    new_words = Counter([i for i in norm_words if i not in db_words])

    for w, c in new_words.items():
        vals = {'word': w, 'count': c, 'user_id': msg_usr_id, 'chat_id': msg_chat_id}
        q = sqlalchemy.insert(Words).values(vals)
        Dbase.conn.execute(q)

    old_words = [(x, y, z) for x, y, z in db_data if y in norm_words]

    for x, y, z in old_words:
        vals = {'count': z + len([i for i in norm_words if i == y])}
        q = sqlalchemy.update(Words).where(Words.id==x).values(vals)
        Dbase.conn.execute(q)