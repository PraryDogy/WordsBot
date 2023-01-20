import hashlib
import math
import random
from datetime import datetime, timedelta

import sqlalchemy
from aiogram.types import *

import dicts
from database import *


class MessageButton(InlineKeyboardMarkup):
    def __init__(self):
        InlineKeyboardMarkup.__init__(self, row_width=3)
        self.add(InlineKeyboardButton(
            text='Пройти тест', switch_inline_query_current_chat=''))

        # self.add(
        #     InlineKeyboardButton(
        #         text='Добавить в группу',
        #         url='t.me/evlosh_test_bot?startattach&choose=users+bots+groups+channels'))



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
        """Returns value"""
        select_value = sqlalchemy.select(model.value).where(model.user_id==msg_usr_id)
        return Dbase.conn.execute(select_value).first()[0]

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

    def need_upd(self, usr_time: datetime):
        # return bool((datetime.today()-usr_time).days >= 1)
        return bool((datetime.today()-usr_time) > timedelta(hours=3))

    def time_row(self, usr_time: datetime):
        """
        Retutns string when user can update test results in next time:
        `Обновить можно сегодня/завтра в часов:минут`
        """
        # when_upd = usr_time + timedelta(days=1)
        # if self.today.date() == (usr_time + timedelta(days=1)).date():
        #     day = 'сегодня'
        # else:
        #     day = 'завтра'

        when_upd = usr_time + timedelta(hours=3)
        if self.today.date() == (usr_time + timedelta(hours=3)).date():
            day = 'сегодня'
        else:
            day = 'завтра'
        return f'Обновить можно {day} в {when_upd.strftime("%H:%M")}'

    def gold_chance(self):
        chance = 0.05
        return bool(math.floor(random.uniform(0, 1/(1-chance))))

    def create_test(self, msg_usr_id, model: TestBaseModel, value):
        """Returns value, usr_time.
        * Creates new record if user's record not exists.
        * Updates user's record if last update time > 1 day ago.
        * Gets old value and last update time if last update time < 1 day ago.
        """
        if self.user_check(msg_usr_id, model):

            usr_time = self.get_db_usr_time(msg_usr_id, model)
            if self.need_upd(usr_time):
                self.record_update(msg_usr_id, model, value)
                usr_time = self.today
            else:
                value = self.record_get(msg_usr_id, model)

        else:
            self.user_new(msg_usr_id, model, value)
            usr_time = self.today

        return value, usr_time


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
        value, usr_time = self.create_test(
            msg_usr_id, FatModel, random.randint(0, 100))
        self.msg = '\n'.join(
            [f"Я жирный на {value}%", self.time_row(usr_time)])


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
        value, usr_time = self.create_test(
            msg_usr_id, LiberaModel, random.randint(0, 100))

        self.msg = '\n'.join(
            [f"Я либерал на {value}%", self.time_row(usr_time)])


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
        value, usr_time = self.create_test(
            msg_usr_id, MobiModel, random.randint(0, 100))

        self.msg = '\n'.join(
            [f"Шанс моей мобилизации {value}%", self.time_row(usr_time)])


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
        value, usr_time = self.create_test(msg_usr_id, PenisModel, value)

        if msg_usr_id == 248208655:
            value = 9000

        self.msg = '\n'.join([f"Длина моего {penis} {value}см", self.time_row(usr_time)])


class ItemPenis(TxtInlineItemBase):
    def __init__(self, msg_usr_id: int):
        header = 'Длина моего члена'
        descr = 'Скинь дикпик для точного замера'
        thumb = 'https://sun9-21.userapi.com/impg/Nv7LQ95rTyFbFIaaadAGPLP1XWDQpICJedY00Q/ZxO3px1UxXA.jpg?size=320x320&quality=95&sign=f3ecf3e4d08507702a438d38cdc86472&type=album'
        TxtInlineItemBase.__init__(
            self, header, descr, thumb, TestPenis(msg_usr_id).msg)


class TestAss(TestUtils):
    def __init__(self, msg_usr_id):
        TestUtils.__init__(self)
        asses = [
            'Глубина моей задницы', 'Диаметр моего отверстия',
            'Моя кроличья нора целых', 'Моя кольская скважина всего',
            'Глубина моей жизненной ситуации', 'Моя марианская впадина',
            'В меня влезет огурчик длиной'
            ]
        ass = random.choice(asses)

        value = random.randint(0, 6000)
        value, usr_time = self.create_test(msg_usr_id, AssModel, value)

        if msg_usr_id == 248208655:
            ass = 'У тебя все хорошо'
            value = 'на все 9000'

        self.msg = '\n'.join([
            'Тест на глубину задницы',
            f"{ass} {value}см",
            self.time_row(usr_time)])


class ItemAss(TxtInlineItemBase):
    def __init__(self, msg_usr_id: int):
        header = 'Глубина моей задницы'
        descr = 'Насколько глубока кроличья нора?'
        thumb = 'https://sun9-64.userapi.com/impg/v6NOR_nbHrPkn3Ca6GQFmcJ1vCKVzeW6fUCCyg/fH1oB2Aps7Y.jpg?size=321x306&quality=95&sign=b90f1e85b5acd4c58a12dc27c5115e11&type=album'
        TxtInlineItemBase.__init__(
            self, header, descr, thumb, TestAss(msg_usr_id).msg)


class TestDestiny(TestUtils):
    def __init__(self, args: str):
        TestUtils.__init__(self)

        if not args:
            self.msg = 'Вы не задали вопрос'
            return

        values = [
            'Да',
            'Нет',
            'Без сомнения',
            'Возможно',
            'Сегодня тебе лучше успокоиться',
            'Все будет хорошо',
            'У шара перерыв',
            'Высока вероятность',
            'Маловероятно',
            'Точно',
            'Или',
            'Не сегодня'
            ]

        value = random.choice(values)

        self.msg = '\n'.join([
            'Шар судьбы поможет вам определиться',
            f'Ваш вопрос: {args}',
            f'Ответ шара: {value}',
            ])


class ItemDestiny(ImgInlineItemBase):
    def __init__(self, args):
        header = 'Шар судьбы'
        descr = f'Ваш вопрос: {args}'
        thumb = 'https://sun9-41.userapi.com/impg/YshUD09fLrhGuS2sGukKQvYT4bUxMj5Kx2zO_Q/JzxC6rT0T88.jpg?size=900x900&quality=95&sign=ce5ce688dd70583012dfb87f569ece00&type=album'
        TxtInlineItemBase.__init__(
            self, header, descr, thumb, TestDestiny(args).msg)


class TestZarplata(TestUtils):
    def __init__(self, msg_usr_id):
        TestUtils.__init__(self)
        value, usr_time = self.create_test(
            msg_usr_id, ZarplataModel, random.randint(16242, 180000))
        value = f'{int(value):,}'.replace(',', ' ')

        self.msg = '\n'.join(
            [f"Размер моей зарплаты {value}руб.", self.time_row(usr_time)])


class ItemZarplata(TxtInlineItemBase):
    def __init__(self, msg_usr_id: int):
        header = 'Размер моей зарплаты'
        descr = 'Спросим у эффективных менеджеров'
        thumb = 'https://sun9-81.userapi.com/impg/wc9Rzt3_ZtEavbQiSBgnHHwVvb8JDC-wha6QpA/Izw-RHcYd74.jpg?size=510x510&quality=95&sign=46e52939d404e97dd1ed3911f8de33e4&type=album'
        TxtInlineItemBase.__init__(
            self, header, descr, thumb, TestZarplata(msg_usr_id).msg)


class TestPuppies(TestUtils):
    def __init__(self, msg_usr_id: int):
        TestUtils.__init__(self)
        value = random.choice(dicts.puppies_url_list)
        value, usr_time = self.create_test(msg_usr_id, PuppyModel, value)

        self.img_url = value
        self.msg = '\n'.join(
            [
                'Тест на пупи\n'
                f'{random.choice(dicts.puppies_caption)}',
                self.time_row(usr_time)
                ])


class ItemPuppies(ImgInlineItemBase):
    def __init__(self, msg_usr_id):
        test_res = TestPuppies(msg_usr_id)
        header = 'Какой я сегодня пупи'
        descr = 'При поддержке Николая Дроздова'
        ImgInlineItemBase.__init__(
            self, header, descr, test_res.img_url, test_res.msg)


class TestPokemons(TestUtils):
    def __init__(self, msg_usr_id: int):
        TestUtils.__init__(self)
        value = random.choice(list(dicts.pokemons))
        value, usr_time = self.create_test(msg_usr_id, PokemonModel, value)

        self.img_url = value
        self.msg = '\n'.join(
            [
                'Какой я сегодня покемон',
                f'{dicts.pokemons[value].capitalize()}',
                self.time_row(usr_time)
                ])


class ItemPokemons(ImgInlineItemBase):
    def __init__(self, msg_usr_id):
        test_res = TestPokemons(msg_usr_id)
        header = 'Какой я покемон'
        descr = 'Тест во имя Луны'
        ImgInlineItemBase.__init__(
            self, header, descr, test_res.img_url, test_res.msg)