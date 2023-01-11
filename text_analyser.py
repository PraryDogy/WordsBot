import string

import spacy
from pymorphy2 import MorphAnalyzer

from dicts import stop_words
from datetime import datetime
import re


'python -m spacy download ru_core_news_md'

print('load spacy model')
nlp = spacy.load("ru_core_news_md")
lemmatizer = MorphAnalyzer()


def normalize_word(word: str):
    return lemmatizer.parse(word)[0].normal_form


def words_regex(message: str):
    """
    Returns tuple of words in lower case, normal form, excluding stopwords and
    links.
    """
    message = message.split()

    words_reg_list = []
    for w in message:

        link = re.match(r'(https?:\/\/[^ ]*)/', w)
        if not link:
            word = re.match(r'(\w+)', w)
            if word:
                words_reg_list.append(word.group(1))

    lema = tuple(normalize_word(w) for w in words_reg_list)
    words = tuple(i for i in lema if i not in stop_words)
    return words


def get_nouns(db_words: tuple):
    """
    Returns tuple of tuples `noun`, `count`.
    * `db_words`: tuple of tuples `word`, `count`
    """
    print('start nouns')
    res = []
    for w, c in db_words:
        doc = nlp(w)
        for word in doc:
            if word.pos_ in ('NOUN', 'PROPN'):
                res.append((word.text, c))
    return res
