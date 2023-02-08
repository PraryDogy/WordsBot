from . import (dec_times_append, dec_times_update_timer, dec_update_user,
               types, words_append, words_update_timer, del_message_append, bot_config)

__all__ = (
    "catch_delete"
    )


async def catch_delete(message: types.Message):
    if message.via_bot:
        if message.via_bot.username == bot_config.bot_name:
            del_message_append(message)
