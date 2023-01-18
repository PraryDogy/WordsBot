import re

import clipboard

print('load spacy model')
import re

import pymorphy2
import spacy

from dicts import *

'python -m spacy download ru_core_news_md'
nlp = spacy.load("ru_core_news_md")
morph = pymorphy2.MorphAnalyzer()


def normalize_word(word: str):
    return [i.lemma_ for i in nlp(word)][0] if word else False


def words_regex(message: str):
    words_reg_list = []
    for w in message.split():

        link = re.match(r'(https?:\/\/[^ ]*)/', w)
        if not link:
            word = re.match(r'(\w+)', w)
            if word:
                words_reg_list.append(word.group(1))

    return words_reg_list


def words_filter(message: str):
    """
    Returns tuple of words in lower case, normal form, excluding stopwords and
    links.
    """
    # message = message.split()
    words_reg_list = words_regex(message)

    lema = tuple(normalize_word(w) for w in words_reg_list)
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


def get_file_id(message):
    reg = r'"file_id": "\S*"'
    res = re.findall(reg, str(message))
    file_id = res[-1].split(' ')[-1].strip('"')
    clipboard.copy(file_id)
    print(file_id)
    return file_id


def khalisi_politic(message: str):
    for rus, eng in ru_eng_abc.items():
        if eng in message:
            message = message.replace(eng, rus)

    words_list = message.lower().split()
    for msg_word in words_list:
        for p_word in politic_words:
            if p_word in msg_word:
                return True
    return False


def khalisi_convert(message: str):
    words_list = message.lower().split()
    new = []
    for msg_word in words_list:
        for src, rpl in khalisi_words.items():
            if src in msg_word and len(msg_word) > 1:
                new.append(msg_word.replace(src, rpl))
                break
    return (' '.join(new))


def destiny_analyse(message):
    message = message.split()
