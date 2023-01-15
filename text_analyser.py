import re

import clipboard

print('load spacy model')
import pymorphy2
import spacy

from dicts import *

'python -m spacy download ru_core_news_md'
nlp = spacy.load("ru_core_news_md")
morph = pymorphy2.MorphAnalyzer()


def normalize_word(word: str):
    return [i.lemma_ for i in nlp(word)][0] if word else False


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


def get_file_id(message):
    reg = r'"file_id": "\S*"'
    res = re.findall(reg, str(message))
    file_id = res[-1].split(' ')[-1].strip('"')
    clipboard.copy(file_id)
    print(file_id)
    return file_id