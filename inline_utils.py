import hashlib
import random
from datetime import datetime, timedelta

import sqlalchemy
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           InlineQueryResultArticle, InlineQueryResultPhoto,
                           InputTextMessageContent, InlineQueryResultCachedGif)

import cfg
from database import Dbase, FatModel, InlineBasemodel, LiberaModel, PuppyModel
from dicts import puppies_url, you_fat, you_libera, you_not_fat, you_not_libera, gifs_id


class TestUtils:
    def __init__(self):
        self.new_value = random.randint(0, 100)
        self.now = datetime.today().replace(microsecond=0)

    def db_usr_check(self, msg_usr_id, model: InlineBasemodel):
        """
        Returns `True` if record already in database else `False`
        """
        select_usr = sqlalchemy.select(model).where(model.user_id==msg_usr_id)
        return bool(Dbase.conn.execute(select_usr).first())

    def get_db_usr_time(self, msg_usr_id: int, model: InlineBasemodel):
        """
        Returns model.time in datetime format.
        """
        select_time = sqlalchemy.select(model.time).where(model.user_id==msg_usr_id)
        res = Dbase.conn.execute(select_time).first()[0]
        return datetime.strptime(res, '%Y-%m-%d %H:%M:%S')

    def msg_create(
        self, phrase_before_value: str, value, phrase_after_value: str,
        phrases_list: list, input_time: datetime):

        next_update_time = input_time + timedelta(days=1)
        if next_update_time.date() <= datetime.today().date():
            day = 'сегодня'
        else:
            day = 'завтра'

        first_row = f'{phrase_before_value} {value} {phrase_after_value}'
        second_row = random.choice(phrases_list)
        third_row = f'Обновить можно {day} в {next_update_time.hour}:{next_update_time.minute}'

        return f'{first_row}\n{second_row}\n{third_row}'

    def insert_record(self, vals, model):
        new_record = sqlalchemy.insert(model).values(vals)
        Dbase.conn.execute(new_record)

    def update_record(self, vals, model: InlineBasemodel, msg_usr_id):
        """Updates database record by model.user_id==msg_usr_id"""
        update_record = sqlalchemy.update(model).where(model.user_id==msg_usr_id).values(vals)
        Dbase.conn.execute(update_record)


class PercentTest(TestUtils):
    def __init__(self, model: InlineBasemodel, msg_usr_id: int,
        phrase_before_value: str, phrase_after_value: str, phrases_list: tuple):
        """
        *`model`: InlineBasemodel
        *`msg_user_id`: user id from tg message
        *`phrase_before_value`: this phrase before `value`
        *`phrase_after_value`: this phrase after `value`
        *`phrases_list`: list of phrases list ( [phrases_list], [phrases_list] )
        
        *`phrases_list[0]`: phrases for value < 50
        *`phrases_list[1]`: phrases for value > 50
        """
        TestUtils.__init__(self)
        phrases_choise = phrases_list[0] if self.new_value < 50 else phrases_list[1]

        if not self.db_usr_check(msg_usr_id, model):
            vals = {'percent':self.new_value, 'time': str(self.now), 'user_id': msg_usr_id}
            self.insert_record(vals, model)

            self.msg = self.msg_create(
                phrase_before_value, self.new_value, phrase_after_value,
                phrases_choise, self.now)
            return

        db_usr_t = self.get_db_usr_time(msg_usr_id, model)
        if (self.now - db_usr_t).days > 0:
            vals = {'percent': self.new_value, 'time': self.now}
            self.update_record(vals, model, msg_usr_id)

            self.msg = self.msg_create(
                phrase_before_value, self.new_value, phrase_after_value,
                phrases_choise, self.now)
        else:
            select_percent = sqlalchemy.select(model.percent).where(model.user_id==msg_usr_id)
            db_usr_percent = Dbase.conn.execute(select_percent).first()[0]
            phrases_choise = phrases_list[0] if db_usr_percent < 50 else phrases_list[1]
            self.msg = self.msg_create(
                phrase_before_value, db_usr_percent, phrase_after_value,
                phrases_choise, db_usr_t)


class PercentFat(PercentTest):
    def __init__(self, msg_user_id):
        PercentTest.__init__(
            self, FatModel, msg_user_id, cfg.fat_before_value, '%',
            (you_not_fat, you_fat))


class PercentLibera(PercentTest):
    def __init__(self, msg_user_id):
        PercentTest.__init__(
            self, LiberaModel, msg_user_id, cfg.libera_before_value, '%',
            (you_not_libera, you_libera))


class MessageButton(InlineKeyboardMarkup):
    def __init__(self):
        InlineKeyboardMarkup.__init__(self, row_width=3)
        self.add(InlineKeyboardButton(
            text='Пройти тест', switch_inline_query_current_chat=''))


class InlineItem:
    def __init__(self, header: str, descr: str, img_path: str, test_result: str):
        """
        *head: test name
        *inline_query: query from aiogram message handler
        *img_path: web url
        """
        head_id: str = hashlib.md5(header.encode()).hexdigest()
        msg = InputTextMessageContent(test_result)

        self.item = InlineQueryResultArticle(
            id=head_id,
            title=f'{header}',
            description=descr,
            input_message_content=msg,
            thumb_url=img_path,
            reply_markup=MessageButton()
            )


class ItemLibera(InlineItem):
    def __init__(self, msg_usr_id: int):
        test_res = PercentLibera(msg_usr_id)
        InlineItem.__init__(self, cfg.libera_header, cfg.libera_descr, cfg.PUTIN_IMG, test_res.msg)


class ItemFat(InlineItem):
    def __init__(self, msg_usr_id: int):
        test_res = PercentFat(msg_usr_id)
        InlineItem.__init__(self, cfg.fat_header, cfg.fat_descr, cfg.FAT_IMG, test_res.msg)



class TestPuppy(TestUtils):
    def __init__(self, msg_usr_id):
        TestUtils.__init__(self)
        self.puppy_url = random.choice(puppies_url)

        if not self.db_usr_check(msg_usr_id, PuppyModel):
            vals = {'url': self.puppy_url, 'time': str(self.now), 'user_id': msg_usr_id}
            self.insert_record(vals, PuppyModel)

        db_usr_t = self.get_db_usr_time(msg_usr_id, PuppyModel)
        if (self.now - db_usr_t).days > 0:
            vals = {'url': self.puppy_url, 'time': self.now}
            self.update_record(vals, PuppyModel, msg_usr_id)
        else:
            select_url = sqlalchemy.select(PuppyModel.url).where(PuppyModel.user_id==msg_usr_id)
            self.puppy_url = Dbase.conn.execute(select_url).first()[0]


class ItemPuppy(TestPuppy):
    def __init__(self, msg_usr_id: int):
        TestPuppy.__init__(self, msg_usr_id)

        self.item = InlineQueryResultPhoto(
            id=hashlib.md5(cfg.puppy_header.encode()).hexdigest(),
            photo_url=self.puppy_url,
            thumb_url=cfg.CAT_IMG,
            title=cfg.puppy_header,
            description=cfg.puppy_descr,
            reply_markup=MessageButton(),
            )
