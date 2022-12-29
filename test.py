import string
import sqlalchemy
from database import Dbase, Users, Words

def sort_words(input: tuple):
    unic_words = set(i[0] for i in input)
    result = []
    for word in unic_words:
        counter = 0
        for w, c in input:
            counter += c if word == w else False
        result.append((word, counter))
    return tuple(reversed(sorted(result, key=lambda x: x[1])))


def chat_words(msg_chat_id):
    q = sqlalchemy.select(Words.word, Words.count).where(
        Words.chat_id==-1001297579871).order_by(-Words.count)
    db_words = Dbase.conn.execute(q).fetchall()
    sorted = sort_words(db_words)[:150]
    return list(i[0] for i in sorted)

restricted = (
    'это', 'что', 'так', 'все', 'как', 'там', 'меня', 'уже', 'вот', 
    'где', 'если', 'есть', 'раз', 'нет', 'мне', 'для', 
    'кто', 'они', 'она', 'тоже', 'чем', 'тебя',
    'его', 'зачем', 'топ', 'или', 
    'ещё', 'тут', 'был', 'нас', 
    'про', 'еще', 'вас', 'чего'
    )


for i in restricted:
    q = sqlalchemy.delete(Words).where(Words.word==i)
    Dbase.conn.execute(q)