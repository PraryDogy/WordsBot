from database import *
import sqlalchemy

q = sqlalchemy.select(Words.chat_id)
res = Dbase.conn.execute(q)

res = [i[0] for i in res]
res = set(res)

print(len(res))