from datetime import datetime, timedelta

import sqlalchemy

from database import Dbase, Users


def user_update_times(user_id: int):
    q = (
        sqlalchemy.select(Users.times)
        .filter(Users.user_id==user_id)
        )
    user_times: str = Dbase.conn.execute(q).first()[0]
    today = str(datetime.today().replace(microsecond=0))

    if not user_times:
        Dbase.conn.execute(
            sqlalchemy.update(Users)
            .filter(Users.user_id==user_id)
            .values(
                {"times": today}
                )
            )

    else:
        Dbase.conn.execute(
            sqlalchemy.update(Users)
            .filter(Users.user_id==user_id)
            .values(
                {"times": f"{user_times},{today}"}
                )
            )

