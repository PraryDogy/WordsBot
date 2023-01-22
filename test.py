from text_analyser import *
from dicts import *
import random

# nlp = spacy.load("ru_core_news_md")



msg = 'что делал слон когда пришел на поле он?'
words_list = words_regex(msg.lower())

for i in words_list:
    if i in dest_q_word:
        print(khalisi_convert(msg))
