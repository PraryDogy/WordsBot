import itertools

import sqlalchemy

from database import Dbase


def sql_unions(queries: list):
    "returns list( dict{ user_id: times(deserialized list) } )"

    SQL_MAX = 300
    q_chunks = [
        queries[i:i+SQL_MAX]
        for i in range(0, len(queries), SQL_MAX)
        ]

    results = [
            Dbase.conn.execute(sqlalchemy.union_all(*q))
            .mappings()
            .fetchall()
        for q in q_chunks
        ]

    return list(itertools.chain.from_iterable(results))