import sqlalchemy
from database import Dbase, Users, Words
from nltk.corpus import stopwords
import pymorphy2


def sort_words(input: tuple):
    unic_words = set(i[0] for i in input)
    result = []
    for word in unic_words:
        counter = 0
        for w, c in input:
            counter += c if word == w else False
        result.append((word, counter))
    return tuple(reversed(sorted(result, key=lambda x: x[1])))


def chat_words():
    q = sqlalchemy.select(Words.word, Words.count).where(
        Words.chat_id==-1001297579871).order_by(-Words.count)
    db_words = Dbase.conn.execute(q).fetchall()
    sorted = sort_words(db_words)
    return list(i[0] for i in sorted)




# stop_words = stopwords.words('russian') + ['это']
# print(stop_words)