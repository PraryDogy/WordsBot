import hashlib
import math
import random
from datetime import datetime, timedelta

import sqlalchemy
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           InlineQueryResultArticle, InlineQueryResultPhoto,
                           InputTextMessageContent)

import dicts
from database import *


class MessageButton(InlineKeyboardMarkup):
    def __init__(self):
        InlineKeyboardMarkup.__init__(self, row_width=3)
        self.add(InlineKeyboardButton(
            text='Пройти тест', switch_inline_query_current_chat=''))


class TestUtils:
    def __init__(self):
        self.today = datetime.today().replace(microsecond=0)

    def user_check(self, msg_usr_id: int, model: TestBaseModel):
        q = sqlalchemy.select(model).where(model.user_id==msg_usr_id)
        return Dbase.conn.execute(q).first()

    def user_new(self, msg_usr_id: int, model: TestBaseModel, new_value):
        vals = {'value': str(new_value), 'time': str(self.today), 'user_id': msg_usr_id}
        new_record = sqlalchemy.insert(model).values(vals)
        Dbase.conn.execute(new_record)

    def record_update(self, msg_usr_id, model: TestBaseModel, new_value):
        vals = {'value': str(new_value), 'time': str(self.today)}
        update_record = sqlalchemy.update(model).where(model.user_id==msg_usr_id).values(vals)
        Dbase.conn.execute(update_record)

    def record_get(self, msg_usr_id, model: TestBaseModel):
        select_value = sqlalchemy.select(model.value).where(model.user_id==msg_usr_id)
        old_value = Dbase.conn.execute(select_value).first()
        return old_value[0] if old_value else False

    def get_db_usr_time(self, msg_usr_id: int, model: TestBaseModel):
        """
        Returns time from database by user_id in datetime format.
        """
        select_time = sqlalchemy.select(model.time).where(model.user_id==msg_usr_id)
        res = Dbase.conn.execute(select_time).first()
        if not res:
            print(f'error get user time{msg_usr_id}')
            return self.today
        return datetime.strptime(res[0], '%Y-%m-%d %H:%M:%S')

    def need_update(self, usr_time: datetime):
        if (self.today - usr_time).days >= 1:
            return True
        return False

    def time_row(self, usr_time: datetime):
        """
        Retutns string when user can update test results in next time:
        `Обновить можно сегодня/завтра в часов:минут`
        """
        if (self.today - usr_time).days >= 1:
            day = 'завтра'
            new_time = self.today + timedelta(days=1)
        else:
            day = 'завтра'
            new_time = usr_time + timedelta(days=1)
        return ''
        return f'Обновить можно {day} в {new_time.strftime("%H:%M")}'

    def gold_chance(self):
        chance = 0.05
        return bool(math.floor(random.uniform(0, 1/(1-chance))))


class ImgTestResult(TestUtils):
    def __init__(self, msg_usr_id, model: TestBaseModel, *args):
        """
        * `args`: img links list, good_words below image
        * `img_url`, `msg`
        """
        TestUtils.__init__(self)
        self.img_url = random.choice(args[0])

        if not self.user_new(msg_usr_id, model, self.img_url) or \
            not self.record_update(msg_usr_id, model, self.img_url):
            
            self.img_url = self.record_get(msg_usr_id, model)

        good_row = random.choice(args[1])
        time_row = self.time_row(self.get_db_usr_time(msg_usr_id, model))
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


class TestFat(TestUtils):
    def __init__(self, msg_usr_id):
        TestUtils.__init__(self)
        value = random.randint(0, 100)

        if self.user_check(msg_usr_id, FatModel):
            usr_time = self.get_db_usr_time(msg_usr_id, FatModel)

            if self.need_update(usr_time):
                self.record_update(msg_usr_id, FatModel, value)

            else:
                value = self.record_get(msg_usr_id, FatModel)

        else:
            self.user_new(msg_usr_id, FatModel, value)
            usr_time = self.today

        self.msg = '\n'.join([f"Я жирный на {value}%", 
        self.time_row(usr_time)])


class ItemFat(TxtInlineItemBase):
    def __init__(self, msg_usr_id: int):
        header = 'Насколько я жирный'
        descr = 'Тест основан на научных методиках'
        thumb = 'https://sun9-40.userapi.com/impg/XEe4VPlF5BvuAYbjZLm3MPamjWIhLrxO66oFEw/f54lKM4s6gU.jpg?size=300x300&quality=95&sign=a347fede0405ca0ec49763ebcb68a413&type=album'
        TxtInlineItemBase.__init__(
            self, header, descr, thumb, TestFat(msg_usr_id).msg)


class TestLibera(TestUtils):
    def __init__(self, msg_usr_id):
        TestUtils.__init__(self)
        value = random.randint(0, 100)

        if self.user_check(msg_usr_id, LiberaModel):
            usr_time = self.get_db_usr_time(msg_usr_id, LiberaModel)

            if self.need_update(usr_time):
                self.record_update(msg_usr_id, LiberaModel, value)

            else:
                value = self.record_get(msg_usr_id, LiberaModel)

        else:
            self.user_new(msg_usr_id, LiberaModel, value)
            usr_time = self.today

        self.msg = '\n'.join([f"Я либерал на {value}%", self.time_row(usr_time)])


class ItemLibera(TxtInlineItemBase):
    def __init__(self, msg_usr_id: int):
        header = 'Насколько я либерал'
        descr = 'Анализ вашего телеграма'
        thumb = 'https://sun1-21.userapi.com/impg/PTLggCAuUejRbw1H-GIjpGjNf73dM7IWhYrsww/x6kavkNNquI.jpg?size=300x300&quality=95&sign=9772535c2cd701e33cae3030464999a9&type=album'
        TxtInlineItemBase.__init__(
            self, header, descr, thumb, TestLibera(msg_usr_id).msg)


class TestMobi(TestUtils):
    def __init__(self, msg_usr_id):
        TestUtils.__init__(self)
        value = random.randint(0, 100)

        if self.user_check(msg_usr_id, MobiModel):
            usr_time = self.get_db_usr_time(msg_usr_id, MobiModel)

            if self.need_update(usr_time):
                self.record_update(msg_usr_id, MobiModel, value)

            else:
                value = self.record_get(msg_usr_id, MobiModel)

        else:
            self.user_new(msg_usr_id, MobiModel, value)
            usr_time = self.today

        self.msg = '\n'.join([f"Шанс моей мобилизации {value}%", self.time_row(usr_time)])


class ItemMobi(TxtInlineItemBase):
    def __init__(self, msg_usr_id: int):
        header = 'Шанс моей мобилизации'
        descr = 'Словлю ли я волну?'
        thumb = 'https://sun9-5.userapi.com/impg/mnJv7OTLrAdMqXUA0e5RC-kBEWMEbijLphmejQ/M8LDDxUhuLQ.jpg?size=508x505&quality=95&sign=21030729d57ec5cd1184d9b83b9b4de8&type=album'
        TxtInlineItemBase.__init__(
            self, header, descr, thumb, TestMobi(msg_usr_id).msg)


class TestPenis(TestUtils):
    def __init__(self, msg_usr_id):
        TestUtils.__init__(self)
        penises = [
            'бантика', 'елдака', 'члена', 'краша', 'сосисона', 'кончика',
            'дружка', 'туза', 'ствола', 'хобота', 'хуя', 'пениса', 'дрына',
            'младшего братика', 'шершавого'
            ]
        penis = random.choice(penises)
        value = 49.5 if self.gold_chance() else random.randint(0, 40)

        if self.user_check(msg_usr_id, MobiModel):
            usr_time = self.get_db_usr_time(msg_usr_id, MobiModel)

            if self.need_update(usr_time):
                self.record_update(msg_usr_id, MobiModel, value)

            else:
                value = self.record_get(msg_usr_id, MobiModel)

        else:
            self.user_new(msg_usr_id, MobiModel, value)
            usr_time = self.today

        if msg_usr_id == 248208655:
            value = 9000

        self.msg = '\n'.join([f"Длина моего {penis} {value}см",
                self.time_row(self.get_db_usr_time(msg_usr_id, MobiModel))])


class ItemPenis(TxtInlineItemBase):
    def __init__(self, msg_usr_id: int):
        header = 'Длина моего члена'
        descr = 'Скинь дикпик для точного замера'
        thumb = 'https://sun9-21.userapi.com/impg/Nv7LQ95rTyFbFIaaadAGPLP1XWDQpICJedY00Q/ZxO3px1UxXA.jpg?size=320x320&quality=95&sign=f3ecf3e4d08507702a438d38cdc86472&type=album'
        TxtInlineItemBase.__init__(
            self, header, descr, thumb, TestPenis(msg_usr_id).msg)


class ImgTestPuppies(ImgTestResult):
    def __init__(self, msg_usr_id: int):
        """`msg`, `img_url`"""
        ImgTestResult.__init__(
            self, msg_usr_id, PuppyModel,
            dicts.puppies_url_list, dicts.puppies_caption)


class ItemPuppy(ImgInlineItemBase):
    def __init__(self, msg_usr_id):
        test_res = ImgTestPuppies(msg_usr_id)
        header = 'Какой я сегодня пупи'
        descr = 'При поддержке Николая Дроздова'
        ImgInlineItemBase.__init__(
            self, header, descr,
            test_res.img_url, test_res.msg)
