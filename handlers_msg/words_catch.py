from . import (BOT_NAME, dec_update_user, del_messages_append,
               del_msg_by_timer, times_db_update_force, times_dict_append,
               types, words_append, words_update_force)

__all__ = (
    "msg_catch_words"
    )


@dec_update_user

async def msg_catch_words(message: types.Message):
    await del_msg_by_timer()

    if message.via_bot:
        if message.via_bot.username == BOT_NAME:
            del_messages_append(message)
        return

    elif message.content_type == "text":

        if words_update_force():
            times_db_update_force()

        words_append(message)
        times_dict_append(message)
