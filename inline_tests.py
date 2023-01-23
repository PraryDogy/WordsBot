import random
from datetime import datetime

import sqlalchemy
from aiogram.types import *

from dicts import *
from database import *
from text_analyser import *
from inline_utils import *


class ItemFat(Utils):
    def __init__(self, user_id, user_time, today, need_update, query):
        super().__init__(user_id, user_time, today, need_update, query)

        header = 'Насколько я жирный'
        descr = 'Тест основан на научных методиках'
        thumb = 'https://sun9-40.userapi.com/impg/XEe4VPlF5BvuAYbjZLm3MPamjWIhLrxO66oFEw/f54lKM4s6gU.jpg?size=300x300&quality=95&sign=a347fede0405ca0ec49763ebcb68a413&type=album'

        values = self.create_test(FatModel, {'value': random.randint(0, 100)})

        msg = '\n'.join(
            [
                'Тест на жир',
                f"Я жирный на {values['value']}%",
                self.time_row()
                ])

        self.item = self.txt_base(header, descr, thumb, msg)


class ItemLibera(Utils):
    def __init__(self, user_id, user_time, today, need_update, query):
        super().__init__(user_id, user_time, today, need_update, query)

        header = 'Насколько я либерал'
        descr = 'Анализ вашего телеграма'
        thumb = 'https://sun1-21.userapi.com/impg/PTLggCAuUejRbw1H-GIjpGjNf73dM7IWhYrsww/x6kavkNNquI.jpg?size=300x300&quality=95&sign=9772535c2cd701e33cae3030464999a9&type=album'

        values = self.create_test(
            LiberaModel,
            {'value': random.randint(0, 100)}
            )

        msg = '\n'.join(
            [
                'Тест на либерала',
                f"Я либерал на {values['value']}%",
                self.time_row()
                ])
        self.item = self.txt_base(header, descr, thumb, msg)


class ItemMobi(Utils):
    def __init__(self, user_id, user_time, today, need_update, query):
        super().__init__(user_id, user_time, today, need_update, query)

        header = 'Шанс моей мобилизации'
        descr = 'Словлю ли я волну?'
        thumb = 'https://sun9-5.userapi.com/impg/mnJv7OTLrAdMqXUA0e5RC-kBEWMEbijLphmejQ/M8LDDxUhuLQ.jpg?size=508x505&quality=95&sign=21030729d57ec5cd1184d9b83b9b4de8&type=album'

        values = self.create_test(
            MobiModel,
            {'value': random.randint(0, 100)}
            )

        msg = '\n'.join(
            [
                'Тест на мобилизацию',
                f"Шанс моей мобилизации {values}%",
                self.time_row()
                ])
        self.item = self.txt_base(header, descr, thumb, msg)


class ItemPenis(Utils):
    def __init__(self, user_id, user_time, today, need_update, query):
        super().__init__(user_id, user_time, today, need_update, query)

        header = 'Длина моего члена'
        descr = 'Скинь дикпик для точного замера'
        thumb = 'https://sun9-21.userapi.com/impg/Nv7LQ95rTyFbFIaaadAGPLP1XWDQpICJedY00Q/ZxO3px1UxXA.jpg?size=320x320&quality=95&sign=f3ecf3e4d08507702a438d38cdc86472&type=album'

        values = self.create_test(
            PenisModel,
            {'value': 49.5 if self.gold_chance() else random.randint(0, 40)}
            )

        msg = '\n'.join(
            [
                'Тест на длину',
                f"Длина моего {random.choice(penis_names)} {values['value']}см",
                self.time_row()
                ])

        self.item = self.txt_base(header, descr, thumb, msg)


class ItemAss(Utils):
    def __init__(self, user_id, user_time, today, need_update, query):
        super().__init__(user_id, user_time, today, need_update, query)

        header = 'Глубина моей задницы'
        descr = 'Насколько глубока кроличья нора?'
        thumb = 'https://sun9-64.userapi.com/impg/v6NOR_nbHrPkn3Ca6GQFmcJ1vCKVzeW6fUCCyg/fH1oB2Aps7Y.jpg?size=321x306&quality=95&sign=b90f1e85b5acd4c58a12dc27c5115e11&type=album'

        values = self.create_test(AssModel,{'value': random.randint(0, 40)})

        msg = '\n'.join([
            'Тест на глубину задницы',
            f"{random.choice(ass_names)} {values['value']}см",
            self.time_row()])

        self.item = self.txt_base(header, descr, thumb, msg)


class ItemDestiny(Utils):
    def __init__(self, user_id, user_time, today, need_update, query):
        super().__init__(user_id, user_time, today, need_update, query)

        header = 'Шар судьбы'
        descr = f'Ваш вопрос: {query}'
        thumb = 'https://sun9-41.userapi.com/impg/YshUD09fLrhGuS2sGukKQvYT4bUxMj5Kx2zO_Q/JzxC6rT0T88.jpg?size=900x900&quality=95&sign=ce5ce688dd70583012dfb87f569ece00&type=album'

        if not query:
            msg = 'Вы не задали вопрос'
            self.item = self.txt_base(header, descr, thumb, msg)
            return

        for word in words_regex(query):
            if word in dest_q_word:
                msg = khalisi_convert(query.lower()).capitalize()
                msg = '\n'.join(
                    [
                    'К шару прилетела Кхалиси, и вот, что они передали:',
                    msg])
                self.item = self.txt_base(header, descr, thumb, msg)
                return

        msg = '\n'.join([
            'Шар судьбы поможет вам определиться',
            f'Ваш вопрос: {query}',
            f'Ответ шара: {random.choice(dest_a_main)}',
            ])
        self.item = self.txt_base(header, descr, thumb, msg)


class ItemZarplata(Utils):
    def __init__(self, user_id, user_time, today, need_update, query):
        super().__init__(user_id, user_time, today, need_update, query)

        header = 'Размер моей зарплаты'
        descr = 'Спросим у эффективных менеджеров'
        thumb = 'https://sun9-81.userapi.com/impg/wc9Rzt3_ZtEavbQiSBgnHHwVvb8JDC-wha6QpA/Izw-RHcYd74.jpg?size=510x510&quality=95&sign=46e52939d404e97dd1ed3911f8de33e4&type=album'

        values = self.create_test(
            ZarplataModel,
            {'value': random.randint(16242, 180000)}
            )

        msg = '\n'.join(
            [
                'Тест на зарплату',
                f"Размер моей зарплаты {str(values['value']).replace(',', ' ')}руб.",
                self.time_row()
                ])

        self.item = self.txt_base(header, descr, thumb, msg)


class ItemPuppies(Utils):
    def __init__(self, user_id, user_time, today, need_update, query):
        super().__init__(user_id, user_time, today, need_update, query)

        header = 'Какой я сегодня пупи'
        descr = 'При поддержке Николая Дроздова'

        values = self.create_test(
            PuppyModel,
            {'value': random.choice(puppies_url_list)}
            )

        msg = '\n'.join(
            [
                'Тест на пупи\n'
                f'{random.choice(puppies_captions)}',
                self.time_row()
                ])

        self.item = self.img_base(header, descr, values['value'], msg)


class ItemPokemons(Utils):
    def __init__(self, user_id, user_time, today, need_update, query):
        super().__init__(user_id, user_time, today, need_update, query)

        header = 'Какой я покемон'
        descr = 'Тест во имя Луны'

        values = self.create_test(
            PokemonModel,
            {'value': random.choice(list(pokemon_dict.keys()))}
            )

        msg = '\n'.join(
            [
                'Тест на покемона',
                f'{pokemon_dict[values["value"]].capitalize()}',
                self.time_row()
                ])

        self.item = self.img_base(header, descr, values['value'], msg)


class ItemVgg(Utils):
    def __init__(self, user_id, user_time, today, need_update, query):
        super().__init__(user_id, user_time, today, need_update, query)

        header = 'Какая у меня мышка'
        descr = 'Король Борат все видит'
        thumb = 'https://sun9-84.userapi.com/impg/Ry8m74bDDGpAq1bD4I3lqvAwIK_BHcLzviJmrw/0M6y3oRE1ek.jpg?size=300x231&quality=95&sign=c9c621121c8b5e7657af74c521d1e12d&type=album'

        values = self.create_test(
            VggModel,
            {
                'value': random.randint(1, 30),
                'vgg_descr': random.choice(list(vggs_dict))
                }
            )

        msg = '\n'.join(
            [
                'Тест на мышку',
                f'Глубина моей мышки {values["value"]}см',
                f'Тип моей мышки: {values["vgg_descr"].capitalize()}. {vggs_dict[values["vgg_descr"]].capitalize()}',
                self.time_row()
                ])

        self.item = self.txt_base(header, descr, thumb, msg)
