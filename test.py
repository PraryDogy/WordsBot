from datetime import datetime
from database_queries import db_chat_words_get


db_words = [('😂', 72), ('просто', 40), ('год', 39), ('вад', 37), ('кстати', 35),
            ('😂', 31), ('андрей', 31), ('день', 29), ('просто', 29), ('большой', 28),
            ('просто', 26), ('кстати', 26), ('просто', 25), ('весь', 25), ('😂😂😂', 25),
            ('хороший', 25), ('мужик', 25), ('хотеть', 25), ('новый', 24), ('вообще', 24)
            ]
db_words = db_chat_words_get(-1001297579871, 2500)


res = []
for u_word in set(i[0] for i in db_words):
    macth_list = tuple((word, id) for word, id in db_words if u_word == word)
    res.append((u_word, sum([i[1] for i in macth_list])))
    res.sort()
res = sorted(res, key = lambda x: x[1], reverse=1)[:10]