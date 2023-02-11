from . import (Dbase, TestBaseModel, hashlib, math, random, sqlalchemy,
               timedelta, types, types, declension_n)

__all__ = (
    "Utils",
    )


class MessageButton(types.InlineKeyboardMarkup):
    def __init__(self, row_width=3, inline_keyboard=None, **kwargs):
        super().__init__(row_width, inline_keyboard, **kwargs)
        self.add(types.InlineKeyboardButton(
            text='Пройти тест', switch_inline_query_current_chat=''))


class Utils:
    def __init__(self, inline_query: types.InlineQuery, user_time, today, need_update):
        self.user_id = inline_query.from_user.id
        self.user_time = user_time
        self.today = today
        self.need_update = need_update

    def user_check(self, model: TestBaseModel):
        q = sqlalchemy.select(model).where(model.user_id==self.user_id)
        return Dbase.conn.execute(q).first()

    def user_new(self, model: TestBaseModel, values: dict):
        """
        values: value: str, other(optional): str
        """
        values.update({'user_id': self.user_id})
        new_record = sqlalchemy.insert(model).values(values)
        Dbase.conn.execute(new_record)

    def record_update(self, model: TestBaseModel, values: dict):
        """
        values: user_id: int, value: str, other(optional): str
        """
        update_record = sqlalchemy.update(model)\
            .where(model.user_id==self.user_id).values(values)
        Dbase.conn.execute(update_record)

    def user_get(self, model: TestBaseModel):
        """Returns user's row as dict"""
        select_value = sqlalchemy.select(model)\
            .where(model.user_id==self.user_id)
        return dict(Dbase.conn.execute(select_value).mappings().first())

    def time_row(self):
        """
        Retutns string when user can update test results in next time:
        `Обновить можно сегодня/завтра в часов:минут`
        """
        if self.need_update:
            tm = f"3 {declension_n('час', 3)}"
        else:
            future = self.user_time + timedelta(hours=3)

            delta = (future - self.today).total_seconds()
            h, m = int(delta // 3600), int(delta % 3600 // 60)

            hour_word = declension_n("час", h)
            minute_word = declension_n("минута", m)
            str_hour = f"{h} {hour_word}" if h > 0 else ""

            tm = f"{str_hour} {m} {minute_word}"

        return f'Обновить можно через {tm}'

    def gold_chance(self):
        chance = 0.05
        return bool(
            math.floor(
                random.uniform(0, 1/(1-chance))
                )
                )

    def create_test(self, model: TestBaseModel, values: dict):
        """
        Returns user database row as dict if test dont need update.
        Else returns dict from args
        """
        if self.user_check(model):
            if self.need_update:
                self.record_update(model, values)
            else:
                return self.user_get(model)
        else:
            self.user_new(model, values)
        return values

    def txt_base(self, header: str, descr: str, thumb_url: str, msg: str):
        """
        * `header`: inline header
        * `descr`: inline description
        * `thumb_url`: inline thumbnail image url
        * `msg`: message from test result
        * `item`
        """
        return types.InlineQueryResultArticle(
            id=hashlib.md5(header.encode()).hexdigest(),
            title=header,
            description=descr,
            thumb_url=thumb_url,
            input_message_content=types.InputTextMessageContent(msg),
            reply_markup=MessageButton(),
            )

    def img_base(self, header: str, descr, img_url, msg):
        """
        * `header`: inline header
        * `descr`: inline description
        * `img_url`: inline image url
        * `msg`: message from test result
        `item`
        """
        return types.InlineQueryResultPhoto(
            id=hashlib.md5(header.encode()).hexdigest(),
            photo_url=img_url,
            thumb_url=img_url,
            title=header,
            description=descr,
            caption=msg,
            reply_markup=MessageButton(),
            )