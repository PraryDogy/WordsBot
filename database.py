import sqlite3

import sqlalchemy.ext.declarative
from sqlalchemy import (Column, ForeignKey, Integer, Text, create_engine,
                        delete, insert, select, update)

import cfg


def create_table_words():
    engine = sqlite3.connect(cfg.DATABASE)
    cur = engine.cursor()
    query = """CREATE TABLE words(
        id INTEGER PRIMARY KEY,
        word STRING,
        count INTEGER,
        user STRING
        )"""
    cur.execute(query)


class Dbase():
    """
    Checks database exists with DbChecker.

    *var conn: database connection
    *var base: declatative_base for models and actions
    """
    __engine = create_engine(
        'sqlite:///' + cfg.DATABASE,
        connect_args={'check_same_thread':False,},
        echo= False
        )
    conn = __engine.connect()
    base = sqlalchemy.ext.declarative.declarative_base()


class Users(Dbase.base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    user_name = Column(Text)


class Words(Dbase.base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(Text)
    count = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    chat_id = Column(Integer)


class InlineBasemodel(Dbase.base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    percent = Column(Integer)
    time = Column(Text)
    user_id = Column(Integer)


class LiberaModel(InlineBasemodel):
    __tablename__ = 'libera'
    user_id = Column(Integer, ForeignKey('users.user_id'))


class FatModel(InlineBasemodel):
    __tablename__ = 'fat'
    user_id = Column(Integer, ForeignKey('users.user_id'))


class PuppyModel(Dbase.base):
    __tablename__ = 'puppies'
    id = Column(Integer, primary_key=True)
    url = Column(Text)
    time = Column(Text)
    user_id = Column(Integer)


def reset_db():
    # Dbase.base.metadata.drop_all(Dbase.conn)
    Dbase.base.metadata.create_all(Dbase.conn)

def rem_words(word: str):
    q = select(Words.id).where(Words.word==word)
    res = Dbase.conn.execute(q).fetchall()
    ids = tuple(i[0] for i in res)

    for i in ids:
        q = delete(Words).where(Words.id==i)
        Dbase.conn.execute(q)
