
from aiogram import types

from utilites import (dec_times_append, dec_times_update_timer,
                      dec_update_user, words_append, words_update_timer)


@dec_update_user

@dec_times_append
@dec_times_update_timer

async def msg_catch_words(message: types.Message):
    words_append(message)
    words_update_timer()
