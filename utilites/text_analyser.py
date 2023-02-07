from . import spacy, pymorphy2, khalisi_words, re, stop_words

__all__ = (
    "khalisi_convert",
    "words_find",
    "words_normalize",
    "words_stopwords",
    "get_nouns",
    )


'python -m spacy download ru_core_news_md'
nlp = spacy.load("ru_core_news_md")
morph = pymorphy2.MorphAnalyzer()


def khalisi_convert(words_list: list):
    for word in words_list:
        for khal_word in khalisi_words:
            if khal_word in word:
                yield(word.replace(khal_word, khalisi_words[khal_word]))
                break


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
        if i not in stop_words:
            yield(i)


def get_nouns(words: list):
    for w in words:
        for word in nlp(w):
            if word.pos_ in ('NOUN', 'PROPN'):
                yield(word.text)

