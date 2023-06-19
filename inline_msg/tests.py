import links

from . import (AssModel, DucksModel, EatModel, FatModel, LiberaModel,
               MobiModel, PenisModel, PokemonModel, PuppyModel, ZarplataModel,
               ass_names, destiny_answers, destiny_questions, ducks_url, food,
               penis_names, pokemons, puppies_url, puppies_words, random,
               types, words_find)
from .utils import Utils

__all__ = (
    "Ass",
    "Destiny",
    "Ducks",
    "Eat",
    "Fat",
    "Libera",
    "Mobi",
    "Penis",
    "Pokemons",
    "Puppies",
    "Zarplata",
    )


gold_users = [
    240950204, #morkowik
    431874154, #christy,
    ]


class Fat(Utils):
    def __init__(self, inline_query: types.InlineQuery, user_time, today, need_update):
        super().__init__(inline_query, user_time, today, need_update)

        header = "Насколько я жирный"
        descr = "Тест основан на научных методиках"
        thumb = links.fat

        values = self.create_test(FatModel, {'value': random.randint(0, 100)})

        if inline_query.from_user.id in gold_users:
            values['value'] = random.randint(0, 10)

        msg = '\n'.join(
            [
                'Тест на жир',
                f"Я жирный на {values['value']}%",
                self.time_row()
                ])

        self.item = self.txt_base(header, descr, thumb, msg)


class Libera(Utils):
    def __init__(self, inline_query: types.InlineQuery, user_time, today, need_update):
        super().__init__(inline_query, user_time, today, need_update)

        header = "Насколько я либерал"
        descr = "Анализ вашего телеграма"
        thumb = links.liberal

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


class Mobi(Utils):
    def __init__(self, inline_query: types.InlineQuery, user_time, today, need_update):
        super().__init__(inline_query, user_time, today, need_update)

        header = "Шанс моей мобилизации"
        descr = "Словлю ли я волну?"
        thumb = links.mobi

        values = self.create_test(
            MobiModel,
            {'value': random.randint(0, 100)}
            )

        msg = '\n'.join(
            [
                'Тест на мобилизацию',
                f"Шанс моей мобилизации {values['value']}%",
                self.time_row()
                ])
        self.item = self.txt_base(header, descr, thumb, msg)


class Penis(Utils):
    def __init__(self, inline_query: types.InlineQuery, user_time, today, need_update):
        super().__init__(inline_query, user_time, today, need_update)

        header = "Длина моего члена"
        descr = "Скинь дикпик для точного замера"
        thumb = links.penis

        values = self.create_test(
            PenisModel,
            {'value': 49.5 if self.gold_chance() else random.randint(0, 40)}
            )

        if inline_query.from_user.id in gold_users:
            values['value'] = random.randint(30, 40)

        msg = '\n'.join(
            [
                'Тест на длину',
                f"Длина моего {random.choice(penis_names)} {values['value']}см",
                self.time_row()
                ])

        self.item = self.txt_base(header, descr, thumb, msg)


class Ass(Utils):
    def __init__(self, inline_query: types.InlineQuery, user_time, today, need_update):
        super().__init__(inline_query, user_time, today, need_update)

        header = "Глубина моей задницы"
        descr = "Насколько глубока кроличья нора?"
        thumb = links.ass

        values = self.create_test(AssModel,{'value': random.randint(0, 40)})

        if inline_query.from_user.id in gold_users:
            values['value'] = random.randint(30, 40)

        msg = '\n'.join([
            'Тест на глубину задницы',
            f"{random.choice(ass_names)} {values['value']}см",
            self.time_row()])

        self.item = self.txt_base(header, descr, thumb, msg)


class Destiny(Utils):
    def __init__(self, inline_query: types.InlineQuery, user_time, today, need_update):
        super().__init__(inline_query, user_time, today, need_update)

        header = "Шар судьбы"
        descr = f"Ваш вопрос: {inline_query.query}"
        thumb = links.destiny

        if not inline_query.query:
            msg = 'Вы не задали вопрос'
            self.item = self.txt_base(header, descr, thumb, msg)
            return

        for word in words_find(inline_query.query.split()):
            if word in destiny_questions:

                msg = '\n'.join([
                    f'Ваш вопрос: {inline_query.query}',
                    'Задайте вопрос на "да" или "нет".'
                    ])

                self.item = self.txt_base(header, descr, thumb, msg)
                return

        msg = '\n'.join([
            'Шар судьбы поможет вам определиться',
            f'Ваш вопрос: {inline_query.query}',
            f'Ответ шара: {random.choice(destiny_answers)}',
            ])
        self.item = self.txt_base(header, descr, thumb, msg)


class Zarplata(Utils):
    def __init__(self, inline_query: types.InlineQuery, user_time, today, need_update):
        super().__init__(inline_query, user_time, today, need_update)

        header = "Размер моей зарплаты"
        descr = "Спросим у эффективных менеджеров"
        thumb = links.zarplata

        values = self.create_test(
            ZarplataModel,
            {'value': random.randint(16242, 180000)}
            )
        
        if inline_query.from_user.id in gold_users:
            values['value'] = random.randint(300000, 1000000)

        msg = '\n'.join(
            [
                'Тест на зарплату',
                f"Размер моей зарплаты {int(values['value']):,} руб.".replace(',', ' '),
                self.time_row()
                ])

        self.item = self.txt_base(header, descr, thumb, msg)


class Puppies(Utils):
    def __init__(self, inline_query: types.InlineQuery, user_time, today, need_update):
        super().__init__(inline_query, user_time, today, need_update)

        header = "Какой я сегодня пупи"
        descr = "При поддержке Николая Дроздова"

        values = self.create_test(
            PuppyModel,
            {'value': random.choice(puppies_url)}
            )

        msg = '\n'.join(
            [
                'Тест на пупи\n'
                f'{random.choice(puppies_words)}',
                self.time_row()
                ])

        self.item = self.img_base(header, descr, values['value'], msg)


class Pokemons(Utils):
    def __init__(self, inline_query: types.InlineQuery, user_time, today, need_update):
        super().__init__(inline_query, user_time, today, need_update)

        header = "Какой я покемон"
        descr = "Тест во имя Луны"

        values = self.create_test(
            PokemonModel,
            {'value': random.choice(list(pokemons.keys()))}
            )

        msg = '\n'.join(
            [
                'Тест на покемона',
                f'{pokemons[values["value"]].capitalize()}',
                self.time_row()
                ])

        self.item = self.img_base(header, descr, values['value'], msg)


class Eat(Utils):
    def __init__(self, inline_query: types.InlineQuery, user_time, today, need_update):
        super().__init__(inline_query, user_time, today, need_update)

        header = "Сколько я могу скушать?"
        descr = "Поможет вести диету"
        thumb = links.eat

        values = self.create_test(
            EatModel,
            {
                'value': random.randint(0, 3000),
                'food_list': ', '.join(random.sample(food, 5)),
            }
        )
    
        msg = '\n'.join(
            [
                "Помощь в диете",
                f"В ближайшие пару часов я могу съесть {values['value']} грамм еды.",
                f"Что я могу съесть: {values['food_list'].lower()}",
                self.time_row()
            ]
        )

        self.item = self.txt_base(header, descr, thumb, msg)


class Ducks(Utils):
    def __init__(self, inline_query: types.InlineQuery, user_time, today, need_update):
        super().__init__(inline_query, user_time, today, need_update)

        header = "Какая я уточка?"
        descr = "Узнай свою красоту"

        new_duck = random.choice(list(ducks_url.keys()))
        values = self.create_test(
            DucksModel,
            {'value': new_duck, 'number': ducks_url[new_duck]}
            )

        msg = '\n'.join(
            [
                "Тест на уточку",
                f"Я уточка №{values['number']}",
                self.time_row()
                ]
                )

        self.item = self.img_base(header, descr, values['value'], msg)
