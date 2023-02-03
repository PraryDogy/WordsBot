import cfg
from start_utils import user_data
from functools import wraps



def dec_words_data(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("i'm write words and return function to next actions")
        return func(**kwargs)

    return wrapper


def dec_user_data(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        kwargs.update(
            user_data(kwargs["user_id"], kwargs["user_name"])
            )
        return func(**kwargs)

    return wrapper


@dec_words_data
@dec_user_data
def handler_func(*args, **kwargs):
    print(kwargs)


handler_func(user_id = cfg.evlosh, user_name = "evlosh", limit = 500)


import tkinter


tkinter.Button()