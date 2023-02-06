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
