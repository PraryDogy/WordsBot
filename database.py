import sqlite3
import sqlalchemy
import sqlalchemy.ext.declarative
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
    __engine = sqlalchemy.create_engine(
        'sqlite:///' + cfg.DATABASE,
        connect_args={'check_same_thread':False,},
        echo= False
        )
    conn = __engine.connect()
    base = sqlalchemy.ext.declarative.declarative_base()


class Users(Dbase.base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_name = sqlalchemy.Column(sqlalchemy.Text)


class Words(Dbase.base):
    __tablename__ = 'words'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    word = sqlalchemy.Column(sqlalchemy.Text)
    count = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.user_id'))
    chat_id = sqlalchemy.Column(sqlalchemy.Integer)


# Dbase.base.metadata.drop_all(Dbase.conn)
# Dbase.base.metadata.create_all(Dbase.conn)

# query = sqlalchemy.select(Words.id).where(Words.word=='это', Words.user_id==5717544572, Words.chat_id==-1001297579871)
# res = Dbase.conn.execute(query).first()
# print(res)
