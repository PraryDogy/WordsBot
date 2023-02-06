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


