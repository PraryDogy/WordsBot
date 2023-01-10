import string

import spacy
from pymorphy2 import MorphAnalyzer

from dicts import stop_words
from datetime import datetime
import re


'python -m spacy download ru_core_news_md'

nlp = spacy.load("ru_core_news_md")
lemmatizer = MorphAnalyzer()


def words_classic(text: str):
    """
    Returns words list without punctuation, stopwords and in normal form.
    """
    start = datetime.now()
    punct = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    rem_punct = text.translate(str.maketrans(punct))
    rem_spaces = rem_punct.split()
    lower = tuple(i.lower() for i in rem_spaces)
    lema = tuple(lemmatizer.parse(word)[0].normal_form for word in lower)
    clean_words= tuple(i for i in lema if i not in stop_words)
    end = datetime.now() - start
    print(end)
    return clean_words


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
    print('running')
    for w, c in db_words:
        doc = nlp(w)
        for word in doc:
            if word.pos_ in ('NOUN', 'PROPN'):
                res.append((word.text, c))
    return res



# with open('test_text.txt', 'r') as file:
#     data = file.read()
# data = 'Я взял это ссылку где-нибудь у Илима https://stackoverflow.com/questions/47637005/handmade-estimator-modifies-parameters-in-init/47637293?noredirect=1#comment82268544_47637293 freed'

# classic = words_classic(data)
# regg = words_regex(data)

# print(regg)