import hashlib
import itertools
import random
from datetime import datetime, timedelta

import sqlalchemy
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           InlineQueryResultArticle, InlineQueryResultPhoto,
                           InputTextMessageContent)

import cfg
from database import *
from dicts import *
from utils import db_chat_usernames_get


class MessageButton(InlineKeyboardMarkup):
    def __init__(self):
        InlineKeyboardMarkup.__init__(self, row_width=3)
        self.add(InlineKeyboardButton(
            text='Пройти тест', switch_inline_query_current_chat=''))


class TestUtils:
    def __init__(self):
        self.now = datetime.today().replace(microsecond=0)

    def db_usr_check(self, msg_usr_id, model: TestBaseModel):
        """
        Returns `True` if record already in database else `False`
        """
        select_usr = sqlalchemy.select(model).where(model.user_id==msg_usr_id)
        return bool(Dbase.conn.execute(select_usr).first())

    def get_db_usr_time(self, msg_usr_id: int, model: TestBaseModel):
        """
        Returns time from database by user_id in datetime format.
        """
        select_time = sqlalchemy.select(model.time).where(model.user_id==msg_usr_id)
        res = Dbase.conn.execute(select_time).first()[0]
        return datetime.strptime(res, '%Y-%m-%d %H:%M:%S')

    def update_record(self, vals, model: TestBaseModel, msg_usr_id):
        """Updates database record by model.user_id==msg_usr_id"""
        update_record = sqlalchemy.update(model).where(model.user_id==msg_usr_id).values(vals)
        Dbase.conn.execute(update_record)

    def msg_test_result(self, msg_usr_id: int, model: TestBaseModel, new_value):
        """
        Creates new record if not exists, updates record if previous record
        was more than 24 hours ago.
        Returns `value`: `str` of test result.
        *`model`: InlineBasemodel.
        *`msg_user_id`: user id from tg message.
        *`new_value`: random value for new test result.
        """
        TestUtils.__init__(self)
        db_user_time = self.get_db_usr_time(msg_usr_id, FatModel)

        if not self.db_usr_check(msg_usr_id, model):
            vals = {'value': str(new_value), 'time': str(self.now), 'user_id': msg_usr_id}
            new_record = sqlalchemy.insert(model).values(vals)
            Dbase.conn.execute(new_record)
            return new_value

        elif (self.now - db_user_time).days > 0:
            vals = {'value': new_value, 'time': self.now}
            self.update_record(vals, model, msg_usr_id)
            return new_value

        else:
            select_percent = sqlalchemy.select(model.value).where(model.user_id==msg_usr_id)
            old_value = Dbase.conn.execute(select_percent).first()[0]
            return old_value

    def msg_time(self, input_time: datetime):
        """
        Retutns string when user can update test results in next time
        """
        next_update_time = input_time + timedelta(days=1)
        if next_update_time.date() <= datetime.today().date():
            day = 'сегодня'
        else:
            day = 'завтра'
        return f'Обновить можно {day} в {next_update_time.strftime("%H:%M")}'


class PercentTestBase(TestUtils):
    def __init__(self, msg_usr_id, db_model: TestBaseModel, *args):
        """
        *`args`: phrase before value, phrases list less, prases list more
        """
        TestUtils.__init__(self)
        new_value = random.choice([i for i in range(100)])
        msg_result = self.msg_test_result(msg_usr_id, db_model, new_value)

        percent_row = f'{args[0]} {msg_result}%'
        good_row = random.choice(args[1] if int(msg_result) < 50 else args[2])
        time_row = self.msg_time(self.get_db_usr_time(msg_usr_id, db_model))
        self.msg = f'{percent_row}\n{good_row}\n{time_row}'


class ImgTestBase(TestUtils):
    def __init__(self, msg_usr_id, db_model: TestBaseModel, *args):
        """
        *`args`: img links list, good_words below image
        """
        TestUtils.__init__(self)
        new_value = random.choice(args[0])
        self.link = self.msg_test_result(msg_usr_id, db_model, new_value)

        good_row = random.choice(args[1])
        time_row = self.msg_time(self.get_db_usr_time(msg_usr_id, FatModel))
        self.msg = f'{good_row}\n{time_row}'


class ItemBase:
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


class ImgItemBase:
    def __init__(self, header: str, descr, img_url, msg):
        self.item = InlineQueryResultPhoto(
            id=hashlib.md5(header.encode()).hexdigest(),
            photo_url=img_url,
            thumb_url=img_url,
            title=header,
            description=descr,
            caption=msg,
            reply_markup=MessageButton(),
            )


class PercentTestFat(PercentTestBase):
    def __init__(self, msg_usr_id):
        PercentTestBase.__init__(
            self, msg_usr_id, FatModel,
            'Я жирный на', fat_less, fat_more
            )


class PercentTestLibera(PercentTestBase):
    def __init__(self, msg_usr_id):
        PercentTestBase.__init__(
            self, msg_usr_id, FatModel,
            'Я либерал на', libera_less, libera_more
            )


class PercentTestMobi(PercentTestBase):
    def __init__(self, msg_usr_id):
        PercentTestBase.__init__(
            self, msg_usr_id, MobiModel,
            'Шанс моей мобилизации', mobi_less, mobi_more
            )


class ImgTestPuppies(ImgTestBase):
    def __init__(self, msg_usr_id: int):
        ImgTestBase.__init__(self, msg_usr_id, PuppyModel,
        puppies_url, puppies_caption)


class ItemLibera(ItemBase):
    def __init__(self, msg_usr_id: int):
        test_res = PercentTestLibera(msg_usr_id)
        ItemBase.__init__(self, cfg.libera_header, cfg.libera_descr, cfg.PUTIN_IMG, test_res.msg)


class ItemFat(ItemBase):
    def __init__(self, msg_usr_id: int):
        test_res = PercentTestFat(msg_usr_id)
        ItemBase.__init__(self, cfg.fat_header, cfg.fat_descr, cfg.FAT_IMG, test_res.msg)

class ItemMobi(ItemBase):
    def __init__(self, msg_usr_id: int):
        test_res = PercentTestMobi(msg_usr_id)
        ItemBase.__init__(self, cfg.mobi_header, cfg.mobi_descr, cfg.MOBI_IMG, test_res.msg)


class ItemPuppy(ImgItemBase):
    def __init__(self, msg_usr_id):
        test_res = ImgTestPuppies(msg_usr_id)
        ImgItemBase.__init__(self, cfg.puppy_header, cfg.puppy_descr, test_res.link, test_res.msg)







# class TestPairing(TestUtils):
#     def __init__(self, msg_usr_id, msg_usrname):
#         TestUtils.__init__(self)
#         self.pair = random.choice(db_chat_usernames_get(msg_usr_id))
#         self.input_time = self.now

#         if not self.db_usr_check(msg_usr_id, PairingModel):
#             vals = {'pair': self.pair, 'time': str(self.now), 'user_id': msg_usr_id}
#             self.insert_record(vals, PairingModel)

#         db_usr_t = self.get_db_usr_time(msg_usr_id, PairingModel)
#         if (self.now - db_usr_t).days > 0:
#             vals = {'pair': self.pair, 'time': self.now}
#             self.update_record(vals, PairingModel, msg_usr_id)

#         else:
#             select_pair = sqlalchemy.select(PairingModel.pair, PairingModel.time).where(PairingModel.user_id==msg_usr_id)
#             res = Dbase.conn.execute(select_pair).first()
#             self.pair, self.input_time = res


#         next_update_time = self.input_time + timedelta(days=1)
#         if next_update_time.date() <= datetime.today().date():
#             day = 'сегодня'
#         else:
#             day = 'завтра'
        
#         first_row = f'@{msg_usrname} ваша пара сегодня @{self.pair}'
#         third_row = f'Обновить можно {day} в {next_update_time.strftime("%H:%M")}'

#         self.msg = f'{first_row}\n{third_row}'


# class PairingItem(TestPairing):
#     def __init__(self, msg_usr_id, msg_usrname):
#         """
#         *head: test name
#         *inline_query: query from aiogram message handler
#         *img_path: web url
#         """
#         TestPairing.__init__(self, msg_usr_id, msg_usrname)
#         head_id: str = hashlib.md5(header.encode()).hexdigest()
#         msg = InputTextMessageContent(test_result)

#         self.item = InlineQueryResultArticle(
#             id=head_id,
#             title=f'{header}',
#             description=descr,
#             input_message_content=msg,
#             thumb_url=img_path,
#             reply_markup=MessageButton()
#             )