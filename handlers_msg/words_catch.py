from . import (bot_name, dec_times_append, dec_times_update_timer,
               dec_update_user, del_messages_timer, for_delete_append, types,
               words_append, words_update_timer)

__all__ = (
    "msg_catch_words"
    )


@dec_update_user

@dec_times_append
@dec_times_update_timer

async def msg_catch_words(message: types.Message):

    await del_messages_timer()

    if message.via_bot:
        if message.via_bot.username == bot_name:
            for_delete_append(message)
        return

    elif message.content_type == "text":
        print("words catch")
        words_append(message)
        words_update_timer()
