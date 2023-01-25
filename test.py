
import re

def words_find(words_list: list):
    words_reg_list = []
    for w in words_list:
        link = re.match(r'(https?:\/\/[^ ]*)/', w)
        if not link:
            word = re.match(r'(\w+)', w)
            if word:
                words_reg_list.append(word.group(1))
    yield(i for i in words_reg_list)


a = words_find('Шла саша по шоссе и сосала сушку'.split())


a = (i for i in range(10))
