import random
import time
from datetime import datetime
from datetime import time as dtime

import sqlalchemy

import cfg
from database import Dbase, FatModel, LiberaModel
from dicts import you_libera, you_not_libera


def good_bad_phrases(percent: int, good_phrases: tuple, bad_phrases: tuple):
    """
    *`good_phrases`: if percent > 50
    *`bad_phrases`: if percent < 50
    """
    if percent >= 50:
        return random.choice(good_phrases)
    else:
        return random.choice(bad_phrases)


def inline_test(**kw):
    """
    *`model`: sqlalchemy declarative base model
    *`msg_user_id`: user id from tg message
    *`good_phrases`: tuple with phrases if percent > 50
    *`bad_phrases`: tuple with phrases if percent < 50
    *`say`: this phrase add to percent

    ```
    <<< inline_test(
        model = Libera, msg_user_id = 12345,
        good_phrases = ["I'm pretty well", "I'm the best"],
        bad_phrases = ["I'm so sad", "I'm sick"],
        say = "I'm sick"
    
    >>> "I'm sick on 56%"
    >>> "I'm so sad"
    ```
    """
    hours24 = 86400
    now = int(time.time())
    percent = random.randint(0, 100)

    q = sqlalchemy.select(kw['model']).where(kw['model'].user_id==kw['msg_user_id'])
    usr_check = bool(Dbase.conn.execute(q).first())
    if not usr_check:

        vals = {'percent':percent, 'time': now, 'user_id': kw['msg_user_id']}
        q = sqlalchemy.insert(kw['model']).values(vals)
        Dbase.conn.execute(q)
        return (
            f'{kw["say"]} {percent}%'
            f'\n{good_bad_phrases(percent, kw["good_phrases"], kw["bad_phrases"])}'
            )

    else:

        q = sqlalchemy.select(kw['model'].time).where(kw['model'].user_id==kw['msg_user_id'])
        db_usr_time = Dbase.conn.execute(q).first()[0]
        if db_usr_time + hours24 < now:

            vals = {'percent': percent, 'time': now}
            q = sqlalchemy.update(kw['model']).where(kw['model'].user_id==kw['msg_user_id']).values(vals)
            Dbase.conn.execute(q)
            return (
                f'{kw["say"]} {percent}%'
                f'\n{good_bad_phrases(percent, kw["good_phrases"], kw["bad_phrases"])}'
                )

        else:
            q = sqlalchemy.select(kw['model'].percent).where(kw['model'].user_id==kw['msg_user_id'])
            usr_percent = Dbase.conn.execute(q).first()[0]

            future_t = db_usr_time + hours24
            midnight = datetime.combine(datetime.today(), dtime.max).timestamp()
            if midnight - future_t < 0:
                today_tomorr = 'завтра'
            else:
                today_tomorr = 'сегодня'

            future_t = datetime.fromtimestamp(future_t)
            future_t = future_t.strftime('%H:%M')

            return (
                f'{kw["say"]} {usr_percent}%'
                f'\n{good_bad_phrases(usr_percent, kw["good_phrases"], kw["bad_phrases"])}'
                f'\nОбновить можно {today_tomorr} в {future_t}'
                )


# tst = inline_test(
#     model=FatModel,
#     msg_user_id=cfg.EVLOSH_ID,
#     say='Я жирный на',
#     good_phrases=libera,
#     bad_phrases=no_libera,
#     )


# print(tst)