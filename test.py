import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy import case

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



from sqlalchemy import bindparam
from collections import Counter

words = {555: ['мама', 'вода', 'вода', 'вода', 'вода', 'вода', 'вода']}
count = dict(Counter(words[555]))

q = (
    sqlalchemy.update(Words)
    .filter(Words.word.in_(count), Words.user_id==555)
    .values({Words.count: case(count, value=Words.word)})
    )

res = Dbase.conn.execute(q)
