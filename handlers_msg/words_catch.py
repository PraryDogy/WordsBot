from . import (bot_name, dec_update_user, del_messages_timer,
               del_messages_append, times_dict_append, times_db_update_force, types,
               words_update, words_append)

__all__ = (
    "msg_catch_words"
    )


@dec_update_user

async def msg_catch_words(message: types.Message):

    await del_messages_timer()

    if message.via_bot:
        if message.via_bot.username == bot_name:
            del_messages_append(message)
        return

    elif message.content_type == "text":

        if words_update():
            print("update words and times by 900 limit")
            times_db_update_force()

        words_append(message)
        times_dict_append(message)
