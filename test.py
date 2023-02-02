import cfg
from start_utils import user_data



def dec_user_data(func):
    def wrapper(**kw):
        kw.update(user_data(kw["user_id"], kw["user_name"]))
        return func(**kw)
    return wrapper


@dec_user_data
def handler_func(**kw):
    print(kw["user_time"])


handler_func(
    user_id = cfg.evlosh,
    user_name = "pter",
    limit = 500
    )
