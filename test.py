from database import Dbase, TestsModel, Users
import bot_config
import sqlalchemy
from datetime import datetime


user = 458774984


q = (
    sqlalchemy.select(TestsModel)
    .filter(TestsModel.user_id==user)
    )
user_tests = Dbase.conn.execute(q).mappings().first()

q = (
    sqlalchemy.select(Users.user_time)
    .filter(Users.user_id == user)
    )

user_time: datetime = Dbase.conn.execute(q).first()

print(user_time)