import random
from database import Dbase, Libera
import time
import datetime
import sqlalchemy


def db_libera(msg_user_id):
    percent = random.randint(0, 100)
    now = int(time.time())
    hours24 = 86400

    hours24 = 5
    msg = f'Вы либеральны на {percent}%'


    q = sqlalchemy.select(Libera).where(Libera.user_id==msg_user_id)
    usr_check = bool(Dbase.conn.execute(q).first())

    if not usr_check:
        vals = {'percent':percent, 'time': now, 'user_id': msg_user_id}
        q = sqlalchemy.insert(Libera).values(vals)
        Dbase.conn.execute(q)

    else:
        q = sqlalchemy.select(Libera.time).where(Libera.user_id==msg_user_id)
        db_usr_time = Dbase.conn.execute(q).first()[0]

        if db_usr_time + hours24 <= now:
            vals = {'percent':percent, 'time': now}
            q = sqlalchemy.update(Libera).where(Libera.user_id==msg_user_id).values(vals)
            Dbase.conn.execute(q)

db_libera(666)