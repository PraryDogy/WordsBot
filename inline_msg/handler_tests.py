from datetime import datetime, timedelta

from aiogram import types

from bot_config import bot
from utilites import UserData, dec_update_user

from .tests import (ItemAss, ItemDestiny, ItemEat, ItemFat, ItemLibera,
                    ItemMobi, ItemPenis, ItemPokemons, ItemPuppies,
                    ItemZarplata, ItemDucks)


@dec_update_user
async def create_msg(inline_query: types.InlineQuery):
    user = UserData(inline_query)
    user_data = user.get_db_user_data()

    today = datetime.today().replace(microsecond=0)
    need_update = bool((today - user_data['user_time']) > timedelta(hours=3))

    if need_update:
        user.update_db_user_time(today)

    items = [
        test(
            inline_query.from_user.id, user_data['user_time'],
            today, need_update, inline_query.query).item
            
            for test in (
                ItemDestiny, ItemPuppies, ItemPokemons, ItemDucks,
                ItemEat,
                ItemFat, ItemPenis, ItemAss, ItemZarplata, ItemLibera,
                ItemMobi
                )
                ]

    await bot.answer_inline_query(
        inline_query.id, results=items, is_personal=True, cache_time=0)