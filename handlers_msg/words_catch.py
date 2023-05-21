from . import (dec_update_user, times_db_update_force,
               times_dict_append, types, words_append, words_update_force)

__all__ = (
    "msg_catch_words"
    )


@dec_update_user

async def msg_catch_words(message: types.Message):
    if message.content_type == "text":

        if words_update_force():
            times_db_update_force()

        words_append(message)
        times_dict_append(message)
