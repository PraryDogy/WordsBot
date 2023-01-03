import random
import time
from datetime import datetime
from datetime import time as dtime

import sqlalchemy

from database import Dbase, Libera
from dicts import libera, no_libera

def libera_words(percent):
    if percent >= 50:
        return random.choice(libera)
    else:
        return random.choice(no_libera)


def libera_func(msg_user_id, msg_username):
    hours24 = 86400
    now = int(time.time())

    percent = random.randint(0, 100)

    q = sqlalchemy.select(Libera).where(Libera.user_id==msg_user_id)
    usr_check = bool(Dbase.conn.execute(q).first())
    if not usr_check:

        vals = {'percent':percent, 'time': now, 'user_id': msg_user_id}
        q = sqlalchemy.insert(Libera).values(vals)
        Dbase.conn.execute(q)
        return (
            f'Вы, @{msg_username}, либеральны на {percent}%'
            f'\n{libera_words(percent)}'
            )

    else:

        q = sqlalchemy.select(Libera.time).where(Libera.user_id==msg_user_id)
        db_usr_time = Dbase.conn.execute(q).first()[0]
        if db_usr_time + hours24 < now:

            vals = {'percent':percent, 'time': now}
            q = sqlalchemy.update(Libera).where(Libera.user_id==msg_user_id).values(vals)
            Dbase.conn.execute(q)
            return (
                f'Вы, @{msg_username}, либеральны на {percent}%'
                f'\n{libera_words(percent)}'
                )

        else:
            q = sqlalchemy.select(Libera.percent).where(Libera.user_id==msg_user_id)
            usr_percent = Dbase.conn.execute(q).first()[0]

            future_t = db_usr_time + hours24
            midnight = datetime.combine(datetime.today(), dtime.max).timestamp()
            if midnight - future_t < 0:
                today_tomorr = 'завтра'
            else:
                today_tomorr = 'завтра'

            future_t = datetime.fromtimestamp(future_t)
            future_t = future_t.strftime('%H:%M')

            return (
                f'Вы, @{msg_username}, либеральны на {usr_percent}%'
                f'\n{libera_words(usr_percent)}'
                f'\nОбновить можно {today_tomorr} в {future_t}'
                )


print(libera_func(666, '123'))