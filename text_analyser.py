import string

import spacy
from pymorphy2 import MorphAnalyzer

from dicts import stop_words


nlp = spacy.load("ru_core_news_md")
lemmatizer = MorphAnalyzer()


def download_rus_model():
    'python -m spacy download ru_core_news_md'


with open('test_text.txt', 'r') as file:
    data = file.read()


def words_convert(text: str):
    """
    Returns words list without punctuation, stopwords and in normal form.
    """
    punct = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    rem_punct = text.translate(str.maketrans(punct))
    rem_spaces = rem_punct.split()
    lower = tuple(i.lower() for i in rem_spaces)
    lema = tuple(lemmatizer.parse(word)[0].normal_form for word in lower)
    clean_words= tuple(i for i in lema if i not in stop_words)
    return clean_words


def nouns(db_words: tuple):
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



# words_list = ' '.join(words_convert(data))
# nns = nouns(words_list)
# print(nns)
