from pymorphy_fix import pymorphy2_311_hotfix

from . import khalisi_words, pymorphy2, re, spacy, stop_words

__all__ = (
    "khalisi_convert",
    "words_find",
    "words_normalize",
    "words_stopwords",
    "get_nouns",
    )


'python -m spacy download ru_core_news_md'

pymorphy2_311_hotfix()
nlp = spacy.load("ru_core_news_md")
morph = pymorphy2.MorphAnalyzer()


def declension_n(word: str, number: int):
    """
    Returns passed word in agreed with number form
    """
    word = morph.parse(word)[0]
    return word.make_agree_with_number(number).word


def get_lexeme(word: str):
    return morph.parse(word)[0].lexeme


def khalisi_convert(words_list: list):
    for word in words_list:
        khalisied = False

        for khal_word in khalisi_words:

            if khal_word in word:
                yield(word.replace(khal_word, khalisi_words[khal_word]))
                khalisied = True
                break
        
        if not khalisied:
            yield(word)

        khalisied = False


def words_find(words_list: list):
    for i in words_list:
        if not re.match(r'http\S+', i):
            try:
                yield re.match(r'[a-zA-Zа-яА-Я]+', i).group(0)
            except AttributeError:
                pass


def words_normalize(words_list: list):
    for i in words_list:
        for x in nlp(i):
            if x:
                yield(x.lemma_)


def words_stopwords(words_list: list):
    for i in words_list:
        if i not in stop_words and len(i) >= 3:
            yield(i)


def get_nouns(words: list):
    for w in words:
        for word in nlp(w):
            if word.pos_ in ('NOUN', 'PROPN'):
                yield(word.text)

