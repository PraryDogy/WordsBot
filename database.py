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
        'sqlite:///' + cfg.DATABASE,
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


class PenisModel(TestBaseModel):
    __tablename__ = 'penis'
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


class Migration:
    def migrate_table(self, name):
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

    def full_migration(self):
        for i in ('libera', 'fat', 'mobi', 'puppies'):
            self.migrate_table(i)


def rem_words(word: str):
    q = sqlalchemy.select(Words.id).where(Words.word==word)
    res = Dbase.conn.execute(q).fetchall()
    ids = tuple(i[0] for i in res)

    for i in ids:
        q = sqlalchemy.delete(Words).where(Words.id==i)
        Dbase.conn.execute(q)


def right_joins():
    q = sqlalchemy.select(Words.word, Words.count).join(
        Users, Users.user_id==Words.user_id).where(
        Users.user_name=='Evlosh').order_by(-Words.count)
    return Dbase.conn.execute(q).all()


print('чтоть это чтото')
vals = {'word': 'чтото'}
q = sqlalchemy.update(Words).filter(Words.word=='чтоть').values(vals)
Dbase.conn.execute(q)

print('чпка это чпок')
vals = {'word': 'чпок'}
q = sqlalchemy.update(Words).filter(Words.word=='чпка').values(vals)
Dbase.conn.execute(q)

print('remove all non alphabetic symbolds and lemm this words')

import re
from text_analyser import normalize_word

q = sqlalchemy.select(Words.id, Words.word)
res = Dbase.conn.execute(q).all()
words_update = []

reg = r'\W'
for id, word in res:
    find = re.findall(reg, word)
    if find:
        for symb in find:
            word = word.replace(symb, '')
        word = normalize_word(word)
        words_update.append((id, word))

print(words_update)

for id, word in words_update:
    q = sqlalchemy.delete(Words).filter(Words.id==id)
    Dbase.conn.execute(q)

print('удали из database.py это говно')