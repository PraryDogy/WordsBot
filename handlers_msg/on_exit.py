from . import (asyncio, dec_times_db_update_force, dec_words_update_force,
               del_msg_by_timer)

__all__ = (
    "on_exit"
    )

@dec_times_db_update_force
@dec_words_update_force
def on_exit_fn(args):
    asyncio.run(del_msg_by_timer())