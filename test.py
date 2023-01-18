from text_analyser import *
from dicts import destiny_question, destiny_answer
import random


def get_question_word(words_list):
    question_type = {}
    for word in words_list:

        for k, v in destiny_question.items():
            if word in v:
                question_type['key'] = k
                parsed = morph.parse(word)[0].tag
                question_type['pos'] = parsed.POS
                question_type['number'] = parsed.number
                question_type['case'] = parsed.case
                question_type['gender'] = parsed.gender
                return question_type


def get_prep(words_list):
    for word in words_list:
        parsed = morph.parse(word)[0].tag.POS
        if parsed == 'PREP':
            return word

message = 'Во сколько лет я умру?'
words_list = words_regex(message.lower())

question_type = get_question_word(words_list)
prep = get_prep(words_list)


answ_src = random.choice(destiny_answer[question_type['key']])
answ_res = []
if prep:
    prep = prep.replace('во', 'в')
    answ_res.append(prep)

for i in answ_src.split():
    parsed = morph.parse(i)[0]

    res = parsed.inflect({
        question_type['number'], question_type['case']})

    if question_type['gender']:
        parsed = morph.parse(res.word)[0]
        res = parsed.inflect({question_type['gender']})

    if res:
        answ_res.append(res.word)
    else:
        answ_res.append(i)

print()
print(message)
print(' '.join(answ_res).capitalize())
print()