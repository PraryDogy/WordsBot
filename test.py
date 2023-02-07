# import itertools
# from collections import Counter
# from datetime import datetime
# from functools import wraps
# from time import time

# import sqlalchemy
# from aiogram import types

# from database import Dbase, Users, Words


# def testing(name):
#     import timeit
#     return timeit.repeat(
#         f"for x in range(100): {name}()",
#         f"from __main__ import {name}",
#         number=10
#         )


import clipboard
from time import sleep

def parse_urls():

    with open('_urls.txt', 'w') as file:
        pass

    paste = '1'
    counter = 0

    while 'google' not in paste:
        new_paste = clipboard.paste()

        if new_paste != paste:

            paste = new_paste

            with open('_urls.txt', 'a') as file:
                file.write(new_paste + '\n')

                counter += 1
                print(counter)
                print('write url')
        
        sleep(0.1)


from datetime import datetime, timedelta
import humanize

humanize.i18n.activate("ru_RU")

user_time = "2023-02-08 00:01:00"
user_time = datetime.strptime(user_time, "%Y-%m-%d %H:%M:%S")
when_update = user_time + timedelta(hours=3)

human = humanize.precisedelta(
    when_update, minimum_unit="seconds", format="%0.0f")
human = human.split(' и ')[0].replace(',', '')

print(human)