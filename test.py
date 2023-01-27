import sqlalchemy
from test_db import *


sq_sum = sqlalchemy.sql.expression.func.sum
sq_count = sqlalchemy.sql.expression.func.count
chat_id = 1

queries = []

for user_id in (1, 2):
    queries.append(
        sqlalchemy.select(
            Words.user_id, sq_sum(Words.count), sq_count(Words.word))
        .filter(
            Words.user_id==user_id, Words.chat_id==chat_id)
        )

query = sqlalchemy.union(*queries)

res = [dict(i) for i in Dbase.conn.execute(query).fetchall()]

print(res)