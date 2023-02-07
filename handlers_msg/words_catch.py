from . import (dec_times_append, dec_times_update_timer, dec_update_user,
               types, words_append, words_update_timer)

__all__ = (
    "msg_catch_words"
    )


@dec_update_user

@dec_times_append
@dec_times_update_timer

async def msg_catch_words(message: types.Message):
    if message.via_bot:
        return
    words_append(message)
    words_update_timer()
