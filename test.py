import pymorphy2
from database_queries import (db_all_usernames_get, db_chat_words_get,
                              db_user_get, db_user_time_get, db_user_words_get,
                              db_word_stat_get, db_sim_words, db_word_count, db_word_people)
import cfg

morph = pymorphy2.MorphAnalyzer()
