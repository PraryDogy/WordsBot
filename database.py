import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime

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
    user_time = Column(DateTime)
    times = Column(Text)


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


class AssModel(TestBaseModel):
    __tablename__ = 'ass'
    user_id = Column(Integer, ForeignKey('users.user_id'))


class ZarplataModel(TestBaseModel):
    __tablename__ = 'zarplata'
    user_id = Column(Integer, ForeignKey('users.user_id'))


class PuppyModel(TestBaseModel):
    __tablename__ = 'puppies'
    user_id = Column(Integer, ForeignKey('users.user_id'))


class PokemonModel(TestBaseModel):
    __tablename__ = 'pokemon'
    user_id = Column(Integer, ForeignKey('users.user_id'))


class EatModel(TestBaseModel):
    __tablename__ = 'eat'
    user_id = Column(Integer)
    food_list = Column(Text)


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
                            "user_id" INTEGER,
                            "user_name" TEXT,
                            "user_time" DATATIME,
                            "times" TEXT
                            )
                            """
        copy_data = f"""INSERT INTO {name} SELECT * FROM {name}_old"""
        # copy_data = f"""INSERT INTO {name} SELECT id, value, user_id FROM {name}_old"""
        comm = """COMMIT"""
        enable_fk = """PRAGMA foreign_keys=off"""
        remove_old = f"""DROP TABLE {name}_old"""

        for i in (
            disable_fk, start_transaction, rename, create_table, copy_data,
            comm, enable_fk, remove_old):
            cur.execute(i)

        conn.commit()


tables = list(Dbase.base.metadata.tables.keys())
[tables.remove(i) for i in ('users', 'words', 'eat')]
Dbase.base.metadata.create_all(Dbase.conn)
