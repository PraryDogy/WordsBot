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
    user_time = Column(Text)


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


class VggModel(TestBaseModel):
    __tablename__ = 'vgg'
    user_id = Column(Integer, ForeignKey('users.user_id'))
    vgg_descr = Column(Text)


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
                            "user_id" INTEGER
                            )
                            """
        # copy_data = f"""INSERT INTO {name} SELECT * FROM {name}_old"""
        copy_data = f"""INSERT INTO {name} SELECT id, value, user_id FROM {name}_old"""
        comm = """COMMIT"""
        enable_fk = """PRAGMA foreign_keys=off"""
        remove_old = f"""DROP TABLE {name}_old"""

        for i in (
            disable_fk, start_transaction, rename, create_table, copy_data,
            comm, enable_fk, remove_old):
            cur.execute(i)

        conn.commit()

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


def remove_dubs(model: TestBaseModel):
    q = sqlalchemy.select(model.id, model.user_id)
    res = Dbase.conn.execute(q).all()
    ids = {}

    for id, usr_id in res:
        if not ids.get(usr_id):
            ids[usr_id] = [id]
        else:
            ids[usr_id].append(id)

    ids_to_rem = {}
    for k, v in ids.items():
        if len(v) > 1:
            ids_to_rem[k] = v[:-1]

    for id_list in ids_to_rem.values():
        for id in id_list:
            q = sqlalchemy.delete(model).where(model.id==id)
            Dbase.conn.execute(q)


tables = list(Dbase.base.metadata.tables.keys())
[tables.remove(i) for i in ('users', 'words')]