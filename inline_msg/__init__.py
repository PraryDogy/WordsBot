import hashlib
import math
import random
from datetime import datetime, timedelta

import humanize
import sqlalchemy
from aiogram import types

from bot_config import bot
from database import (AssModel, Dbase, DucksModel, EatModel, FatModel,
                      LiberaModel, MobiModel, PenisModel, PokemonModel,
                      PuppyModel, TestBaseModel, ZarplataModel)
from dicts import *
from utilites import UserData, dec_update_user, words_find

from .create_inline import create_msg as create_inline

humanize.i18n.activate("ru_RU")

__all__ = (
    "create_inline",
    )