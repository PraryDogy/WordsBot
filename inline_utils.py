import hashlib
import random
import time
from datetime import datetime
from datetime import time as dtime

import sqlalchemy
from aiogram.types import (InlineQuery, InlineQueryResultArticle,
                           InputTextMessageContent)

import cfg
from database import Dbase, FatModel, InlineBasemodel, LiberaModel
from dicts import you_fat, you_libera, you_not_fat, you_not_libera


class PercentBase:
    def __init__(self, model: InlineBasemodel, msg_usr_id: int,
        phrase: str, dicts1: tuple, dicts2: tuple):
        """
        *`model`: InlineBasemodel
        *`msg_user_id`: user id from tg message
        *`phrase`: this phrase add to percent
        *`dict1`: tuple with phrases if percent > 50
        *`dict2`: tuple with phrases if percent < 50
        """
        hours24 = 86400
        now = int(time.time())
        new_value = random.randint(0, 100)

        q = sqlalchemy.select(model).where(model.user_id==msg_usr_id)
        if not bool(Dbase.conn.execute(q).first()):

            vals = {'percent':new_value, 'time': now, 'user_id': msg_usr_id}
            q = sqlalchemy.insert(model).values(vals)
            Dbase.conn.execute(q)
            self.msg = f'{phrase} {new_value}%'\
                f'\n{random.choice(dicts1) if new_value > 50 else random.choice(dicts2)}'

        else:
            q = sqlalchemy.select(model.time).where(model.user_id==msg_usr_id)
            db_usr_time = Dbase.conn.execute(q).first()[0]
            if db_usr_time + hours24 < now:

                vals = {'percent': new_value, 'time': now}
                q = sqlalchemy.update(model).where(model.user_id==msg_usr_id).values(vals)
                Dbase.conn.execute(q)

                self.msg = f'{phrase} {new_value}%'\
                    f'\n{random.choice(dicts1) if new_value > 50 else random.choice(dicts2)}'

            else:
                q = sqlalchemy.select(model.percent).where(model.user_id==msg_usr_id)
                db_usr_value = Dbase.conn.execute(q).first()[0]

                next_update = db_usr_time + hours24
                midnight = datetime.combine(datetime.today(), dtime.max).timestamp()
                if midnight - next_update < 0:
                    today_tomorr = 'завтра'
                else:
                    today_tomorr = 'сегодня'

                clock = datetime.fromtimestamp(next_update).strftime('%H:%M')

                self.msg = f'{phrase} {db_usr_value}%'\
                    f'\n{random.choice(dicts1) if db_usr_value > 50 else random.choice(dicts2)}'\
                    f'\nОбновить можно {today_tomorr} в {clock}'


class PercentFat(PercentBase):
    def __init__(self, msg_user_id):
        PercentBase.__init__(self, FatModel, msg_user_id, cfg.fat_msg,
            you_fat, you_not_fat)


class PercentLibera(PercentBase):
    def __init__(self, msg_user_id):
        PercentBase.__init__(self, LiberaModel, msg_user_id, cfg.libera_msg,
            you_libera, you_not_libera)


class ItemBase:
    def __init__(self, header: str, descr: str, img_path: str, test_result: PercentBase):
        """
        *head: test name
        *inline_query: query from aiogram message handler
        *img_path: web url
        """
        head_id: str = hashlib.md5(header.encode()).hexdigest()
        msg = InputTextMessageContent(test_result.msg)

        self.item = InlineQueryResultArticle(
            id=head_id,
            title=f'{header}',
            description=descr,
            input_message_content=msg,
            thumb_url=img_path)


class ItemLibera(ItemBase):
    def __init__(self, msg_usr_id: int):
        test_res = PercentLibera(msg_usr_id)
        ItemBase.__init__(self, cfg.libera_header, cfg.libera_descr, cfg.PUTIN_IMG, test_res)


class ItemFat(ItemBase):
    def __init__(self, msg_usr_id: int):
        test_res = PercentFat(msg_usr_id)
        ItemBase.__init__(self, cfg.fat_header, cfg.fat_descr, cfg.FAT_IMG, test_res)