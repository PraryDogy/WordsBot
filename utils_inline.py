import hashlib
import itertools
import random
from datetime import datetime, timedelta

import sqlalchemy
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           InlineQueryResultArticle, InlineQueryResultPhoto,
                           InputTextMessageContent, InlineQueryResultCachedPhoto, InlineQueryResultCachedGif)

import cfg
from database import *
import dicts


class MessageButton(InlineKeyboardMarkup):
    def __init__(self):
        InlineKeyboardMarkup.__init__(self, row_width=3)
        self.add(InlineKeyboardButton(
            text='Пройти тест', switch_inline_query_current_chat=''))


class TestUtils:
    def get_db_usr_time(self, msg_usr_id: int, model: TestBaseModel):
        """
        Returns time from database by user_id in datetime format.
        """
        select_time = sqlalchemy.select(model.time).where(model.user_id==msg_usr_id)
        res = Dbase.conn.execute(select_time).first()
        if not res:
            print(f'error get user time{msg_usr_id}')
            return datetime.today().replace(microsecond=0)
        return datetime.strptime(res[0], '%Y-%m-%d %H:%M:%S')

    def new_user(self, msg_usr_id, model, new_value):
        """
        Returns True if user is new and new record was created. Else returns False.
        * `msg_usr_id`: telegram message user id
        * `model`: database model for any bot test (e.g: FatModel, PuppyModel)
        * `new_value`: value for any bot test result (e.g: 0-100, img_url)
        """
        select_usr = sqlalchemy.select(model).where(model.user_id==msg_usr_id)
        if not bool(Dbase.conn.execute(select_usr).first()):

            today = datetime.today().replace(microsecond=0)
            vals = {'value': str(new_value), 'time': str(today), 'user_id': msg_usr_id}

            new_record = sqlalchemy.insert(model).values(vals)
            Dbase.conn.execute(new_record)

            return True
        return False

    def update_user(self, msg_usr_id, model: TestBaseModel, new_value):
        """
        Returns True if exist user record was updated. Else returns False.
        Compares `now` time and time when user record was updated `last time`.
        If user record updated more than `one day ago` - updates record with
        `new_value`.

        * `msg_usr_id`: telegram message user id
        * `model`: database model for any bot test (e.g: FatModel, PuppyModel)
        * `new_value`: value for any bot test result (e.g: 0-100, img_url)
        """
        today = datetime.today().replace(microsecond=0)
        db_user_time = self.get_db_usr_time(msg_usr_id, model)

        if (today - db_user_time).days > 0:
            vals = {'value': new_value, 'time': today}
            
            update_record = sqlalchemy.update(model).where(model.user_id==msg_usr_id).values(vals)
            Dbase.conn.execute(update_record)

            return True
        return False

    def get_old_value(self, msg_usr_id, model: TestBaseModel):
        """
        Get value for user from database. 
        """
        select_value = sqlalchemy.select(model.value).where(model.user_id==msg_usr_id)
        old_value = Dbase.conn.execute(select_value).first()
        if old_value:
            return old_value[0]
        return False

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


class PercentTestResult(TestUtils):
    def __init__(self, msg_usr_id, model: TestBaseModel, *args):
        """
        * `args`: phrase before value, phrases list less, phrases list more
        * `msg`
        """
        TestUtils.__init__(self)
        test_result = random.choice([i for i in range(100)])

        if self.new_user(msg_usr_id, model, test_result):
            print('new_user')

        elif self.update_user(msg_usr_id, model, test_result):
            print('update user record')

        else:
            test_result = self.get_old_value(msg_usr_id, model)

        percent_row = f'{args[0]} {test_result}%'
        good_row = random.choice(args[1] if int(test_result) < 50 else args[2])
        time_row = self.msg_time(self.get_db_usr_time(msg_usr_id, model))

        self.msg = f'{percent_row}\n{good_row}\n{time_row}'


class ImgTestResult(TestUtils):
    def __init__(self, msg_usr_id, model: TestBaseModel, *args):
        """
        * `args`: img links list, good_words below image
        * `img_url`, `msg`
        """
        TestUtils.__init__(self)
        self.img_url = random.choice(args[0])

        if self.new_user(msg_usr_id, model, self.img_url):
            print('new_user')

        elif self.update_user(msg_usr_id, model, self.img_url):
            print('update user record')

        else:
            self.img_url = self.get_old_value(msg_usr_id, model)

        good_row = random.choice(args[1])
        time_row = self.msg_time(self.get_db_usr_time(msg_usr_id, model))

        self.msg = f'{good_row}\n{time_row}'


class TxtInlineItemBase:
    def __init__(self, header: str, descr: str, thumb_url: str, msg: str):
        """
        * `header`: inline header
        * `descr`: inline description
        * `thumb_url`: inline thumbnail image url
        * `msg`: message from test result
        * `item`
        """
        self.item = InlineQueryResultArticle(

            id=hashlib.md5(header.encode()).hexdigest(),

            title=header,
            description=descr,
            thumb_url=thumb_url,

            input_message_content=InputTextMessageContent(msg),
            reply_markup=MessageButton()
            )


class ImgInlineItemBase:
    def __init__(self, header: str, descr, img_url, msg):
        """
        * `header`: inline header
        * `descr`: inline description
        * `img_url`: inline image url
        * `msg`: message from test result
        `item`
        """
        self.item = InlineQueryResultPhoto(

            id=hashlib.md5(header.encode()).hexdigest(),

            photo_url=img_url,
            thumb_url=img_url,

            title=header,
            description=descr,

            caption=msg,
            reply_markup=MessageButton(),
            )


class PercentTestFat(PercentTestResult):
    def __init__(self, msg_usr_id):
        """`msg`"""
        PercentTestResult.__init__(
            self, msg_usr_id, FatModel,
            'Я жирный на', dicts.fat_less, dicts.fat_more
            )


class PercentTestLibera(PercentTestResult):
    def __init__(self, msg_usr_id):
        """`msg`"""
        PercentTestResult.__init__(
            self, msg_usr_id, LiberaModel,
            'Я либерал на', dicts.libera_less, dicts.libera_more
            )


class PercentTestMobi(PercentTestResult):
    def __init__(self, msg_usr_id):
        """`msg`"""
        PercentTestResult.__init__(
            self, msg_usr_id, MobiModel,
            'Шанс моей мобилизации', dicts.mobi_less, dicts.mobi_more
            )


class ImgTestPuppies(ImgTestResult):
    def __init__(self, msg_usr_id: int):
        """`msg`, `img_url`"""
        ImgTestResult.__init__(self, msg_usr_id, PuppyModel,
        dicts.puppies_url, dicts.puppies_caption)


class ItemLibera(TxtInlineItemBase):
    def __init__(self, msg_usr_id: int):
        test_res = PercentTestLibera(msg_usr_id)
        TxtInlineItemBase.__init__(
            self, cfg.libera_header, cfg.libera_descr, cfg.PUTIN_IMG, test_res.msg)


class ItemFat(TxtInlineItemBase):
    def __init__(self, msg_usr_id: int):
        test_res = PercentTestFat(msg_usr_id)
        TxtInlineItemBase.__init__(
            self, cfg.fat_header, cfg.fat_descr, cfg.FAT_IMG, test_res.msg)


class ItemMobi(TxtInlineItemBase):
    def __init__(self, msg_usr_id: int):
        test_res = PercentTestMobi(msg_usr_id)
        TxtInlineItemBase.__init__(
            self, cfg.mobi_header, cfg.mobi_descr, cfg.MOBI_IMG, test_res.msg)


class ItemPuppy(ImgInlineItemBase):
    def __init__(self, msg_usr_id):
        test_res = ImgTestPuppies(msg_usr_id)
        ImgInlineItemBase.__init__(
            self, cfg.puppy_header, cfg.puppy_descr, 
            test_res.img_url, test_res.msg)



class ItemTest():
    def __init__(self, msg_usr_id):
        img_id = 'AgACAgIAAx0CYSXtmQACA4FjucZbUASUeaKzFwI1jixw5bEeIQACzsAxGwvOyUkYlYOUkOrG5QEAAwIAA20AAy0E'
        header = 'test'
        self.item = InlineQueryResultCachedPhoto(
            id=hashlib.md5(header.encode()).hexdigest(),
            photo_file_id=img_id,
            title="Untitled",
            description="Untitled",
            caption='test caption',
            reply_markup=MessageButton(),
            )


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


