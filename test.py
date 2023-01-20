from text_analyser import *
from dicts import dest_question, dest_answer
import random
nlp = spacy.load("ru_core_news_md")



class DestinyLang:
    def __init__(self, message):
        self.words = words_regex(message.lower())

        self.prep = []
        self.anwers_list = []

        self.get_question_word()
        self.get_prep()
        self.convert_answer()

    def get_question_word(self):
        for word in self.words:
            for k, v in dest_question.items():
                if word in v:
                    self.src_word = morph.parse(word)[0].tag
                    self.anwers_list = dest_answer[k]
                    return
    
    def get_prep(self):
        for word in self.words:
            if  morph.parse(word)[0].tag.POS == 'PREP':
                self.prep.append(word.replace('во', 'в'))
                return

    def convert_answer(self):
        answer = random.choice(self.anwers_list)
        answer = 'конь'
        words_list = answer.split()

        props = (self.src_word.case, self.src_word.number, self.src_word.gender)
        self.new_answer = []

        for i in words_list:
            parsed = morph.parse(i)[0]

            if parsed.tag.POS in ('NOUN', 'ADJF', 'ADJS', 'PRTF', 'PRTS'): \
                # and 'inan' not in parsed.tag:
                res = parsed.inflect({*props})
                print(res)
                self.new_answer.append(parsed.inflect({*props}).word)
            else:
                self.new_answer.append(i)

    def create_answer(self):
        return (' '.join(self.prep + self.new_answer)).capitalize()

# a = DestinyLang('чей мнения тут не хватает?')
# print(a.create_answer())


from datetime import datetime, timedelta

today = datetime.today().replace(microsecond=0)
usr_time = '2023-01-20 9:55:00'
usr_time = datetime.strptime(usr_time, '%Y-%m-%d %H:%M:%S')
# a = bool((today - usr_time) > timedelta(hours=3))


when_upd = usr_time + timedelta(hours=3)
if today.date() == (usr_time + timedelta(hours=3)).date():
    day = 'сегодня'
else:
    day = 'завтра'
a = f'Обновить можно {day} в {when_upd.strftime("%H:%M")}'


print(a)