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


def download_ntlk(module: str):
    import nltk
    import ssl
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    nltk.download(module)


def lemmatize_text(tokens):
    lemmatizer = pymorphy2.MorphAnalyzer()
    lem_words = []
    for word in tokens:
        lem_words.append(lemmatizer.parse(word)[0].normal_form)
    return lem_words
