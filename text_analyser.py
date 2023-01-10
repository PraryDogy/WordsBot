import string

import spacy
from pymorphy2 import MorphAnalyzer

from dicts import stop_words
from datetime import datetime
import re


'python -m spacy download ru_core_news_md'

nlp = spacy.load("ru_core_news_md")
lemmatizer = MorphAnalyzer()


def words_regex(message: str):
    """
    Returns tuple of words in lower case, normal form, excluding stopwords and
    links.
    """
    message = message.split()

    res = []
    for w in message:

        link = re.match(r'(https?:\/\/[^ ]*)/', w)
        if not link:
            word = re.match(r'(\w+)', w)
            if word:
                res.append(word.group(1))

    lema = tuple(lemmatizer.parse(word)[0].normal_form for word in res)
    words = tuple(i for i in lema if i not in stop_words)
    return words


def get_nouns(db_words: tuple):
    """
    Returns tuple of tuples `noun`, `count`.
    * `db_words`: tuple of tuples `word`, `count`
    """
    res = []
    for w, c in db_words:
        doc = nlp(w)
        for word in doc:
            if word.pos_ in ('NOUN', 'PROPN'):
                res.append((word.text, c))
    return res
