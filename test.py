# import sqlalchemy
# import sqlalchemy.ext.declarative
# from sqlalchemy import Column, ForeignKey, Integer, Text

# import cfg
# from database import Words
# from text_analyser import get_nouns


# class Dbase():
#     """
#     Checks database exists with DbChecker.

#     *var conn: database connection
#     *var base: declatative_base for models and actions
#     """
#     engine = sqlalchemy.create_engine(
#         'sqlite:///' + 'test_db.db',
#         connect_args={'check_same_thread':False,},
#         echo= False
#         )
#     conn = engine.connect()
#     base = sqlalchemy.ext.declarative.declarative_base()
#     sq_sum = sqlalchemy.sql.expression.func.sum
#     sq_count = sqlalchemy.sql.expression.func.count
#     sq_lower = sqlalchemy.func.lower

