import re

print('load spacy model')
import re

import pymorphy2
import spacy

from dicts import *

'python -m spacy download ru_core_news_md'
nlp = spacy.load("ru_core_news_md")
morph = pymorphy2.MorphAnalyzer()


def words_find(words_list: list):
    words_reg_list = []
    for w in words_list:
        link = re.match(r'(https?:\/\/[^ ]*)/', w)
        if not link:
            word = re.match(r'(\w+)', w)
            if word:
                words_reg_list.append(word.group(1))
    return words_reg_list


def words_normalize(words_list: list):
    """
    Returns list of words in lower case, normal form.
    """
    norm_words = []
    for i in words_list:
        for x in nlp(i):
            norm_words.append(x.lemma_) if x else False
    return norm_words


def words_stopwords(words_list: list):
    return [i for i in words_list if i not in stop_words]


def get_nouns(words: list):
    """
    Returns nouns list.
    """
    res = []
    for w in words:
        for word in nlp(w):
            if word.pos_ in ('NOUN', 'PROPN'):
                res.append(word.text)
    return res


def khalisi_convert(message: str):
    words_list = message.lower().split()
    new = []
    for msg_word in words_list:
        for src, rpl in khalisi_words.items():
            if src in msg_word and len(msg_word) > 1:
                new.append(msg_word.replace(src, rpl))
                break
    return (' '.join(new))
