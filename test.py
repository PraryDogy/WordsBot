import random
import time
from datetime import datetime
from datetime import time as dtime

import sqlalchemy

from database import Dbase, Libera
from dicts import libera, no_libera
from utils import words_convert


def zelek(msg):
    words = words_convert(msg)
    zelen = 'зеленск'
    for w in words:
        if zelen in w:
            return True
    return False
