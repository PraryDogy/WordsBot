import spacy
from nltk.tokenize import RegexpTokenizer
import string
import re
from datetime import datetime

top_words = "мочь просто хороший весь знать год вообще хотеть говорит большой"

with open('test_text.txt', 'r') as file:
    data = file.read()

def words_convert(text: str):
    punct = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    rem_punct = text.translate(str.maketrans(punct))
    rem_spaces = " ".join(rem_punct.split())
    lower = rem_spaces.lower()

    return lower


# def nouns(text):
#     nlp = spacy.load("ru_core_news_md")
#     doc = nlp(text)

#     for token in doc:
#         print(token.text, token.pos_)

