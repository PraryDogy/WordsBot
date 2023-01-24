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




def user_words_write(user_id, chat_id, word_list):
    q = (
        sqlalchemy.select(Words.word, Words.count).
        filter(Words.user_id==555, Words.chat_id==chat_id, Words.word.in_(word_list))
        )

    db_words = dict(Dbase.conn.execute(q).all())
    msg_words = dict(Counter(word_list))
    count = {k: db_words[k] + msg_words[k] for k in (db_words)}

    q = (
        sqlalchemy.update(Words)
        .filter(Words.word.in_(count), Words.user_id==user_id)
        .values({Words.count: case(count, value=Words.word)})
        )
    Dbase.conn.execute(q)

    new_words = [i for i in word_list if i not in db_words]
    count = dict(Counter(new_words))
    values = [{
        'word': x, 'count': y,
        'user_id': user_id, 'chat_id': chat_id
        } for x, y in count.items()]

    if values:
        q = sqlalchemy.insert(Words).values(values)
        Dbase.conn.execute(q)

# word_list = ['мама', 'мама', 'мама', 'вода', 'вода', 'вода', 'масло', 'жрачка', 'масло', 'масло', 'хуйня', 'лох']
# user_words_write(user_id=555, chat_id=123, word_list=word_list)



