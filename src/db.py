"""module for working with sqlite databases"""

import sqlite3
from typing import Tuple


def query_db(path: str, query: str, args: Tuple = (), one: bool = False):
    """function for executing SQL"""
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(query, args)
    db.commit()
    rv = cur.fetchall()
    cur.close()
    db.close()
    return (rv[0] if rv else None) if one else rv


def read_sql(path: str):
    """function for reading SQL files"""
    result = ''
    with open(path, encoding="utf-8") as file:
        result = file.read()
    return result


def drop_table(path: str, name: str) -> None:
    """function for deleting tables"""
    sql = f"DROP TABLE IF EXISTS {name}"
    query_db(path, sql)


def table_sql(path: str, name: str):
    """function to get table sql"""
    sql = """
          SELECT sql
            FROM sqlite_master
           WHERE name = ?
          """
    result = query_db(path, sql, args=(name,), one=True)
    return list(result)[0]


def tables(path: str) -> str:
    """function to get table names"""
    sql = """
          SELECT name
            FROM sqlite_master
           WHERE type = ?
          """
    result = query_db(path, sql, args=("table",))
    result_t = list(map(lambda x: " ".join(list(x)), result))
    return " ".join(result_t)
