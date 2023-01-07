import sqlite3

import sqlalchemy.ext.declarative
from sqlalchemy import (Column, ForeignKey, Integer, Text, create_engine,
                        delete, insert, select, update)

import cfg


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
    last_time = Column(Text)


class Words(Dbase.base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(Text)
    count = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    chat_id = Column(Integer)


class TestBaseModel(Dbase.base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    value = Column(Text)
    time = Column(Text)
    user_id = Column(Integer)


class LiberaModel(TestBaseModel):
    __tablename__ = 'libera'
    user_id = Column(Integer, ForeignKey('users.user_id'))


class FatModel(TestBaseModel):
    __tablename__ = 'fat'
    user_id = Column(Integer, ForeignKey('users.user_id'))


class MobiModel(TestBaseModel):
    __tablename__ = 'mobi'
    user_id = Column(Integer, ForeignKey('users.user_id'))


class PuppyModel(TestBaseModel):
    __tablename__ = 'puppies'
    user_id = Column(Integer, ForeignKey('users.user_id'))


class PairingModel(Dbase.base):
    __tablename__ = 'pairing'
    id = Column(Integer, primary_key=True)
    pair = Column(Text)
    time = Column(Text)
    user_id = Column(Integer)


def rem_words(word: str):
    q = select(Words.id).where(Words.word==word)
    res = Dbase.conn.execute(q).fetchall()
    ids = tuple(i[0] for i in res)

    for i in ids:
        q = delete(Words).where(Words.id==i)
        Dbase.conn.execute(q)


def migrate_table(name):
    import sqlite3

    conn = sqlite3.connect(cfg.DATABASE)
    cur = conn.cursor()

    disable_fk = """PRAGMA foreign_keys=off"""
    start_transaction = """BEGIN TRANSACTION"""
    rename = f"""ALTER TABLE {name} RENAME TO {name}_old"""
    create_table = f"""CREATE TABLE IF NOT EXISTS {name} (
                        "id" INTEGER NOT NULL PRIMARY KEY,
                        "value" TEXT,
                        "time" TEXT,
                        "user_id" INTEGER,
                        FOREIGN KEY ("user_id")REFERENCES "users"("user_id")
                        )
                        """
    copy_data = f"""INSERT INTO {name} SELECT * FROM {name}_old"""
    comm = """COMMIT"""
    enable_fk = """PRAGMA foreign_keys=off"""
    remove_old = f"""DROP TABLE {name}_old"""

    for i in (
        disable_fk, start_transaction, rename, create_table, copy_data,
        comm, enable_fk, remove_old):
        cur.execute(i)

    conn.commit()


def full_migration():
    for i in ('libera', 'fat', 'mobi', 'puppies'):
        migrate_table(i)


Dbase.base.metadata.create_all(Dbase.conn)
