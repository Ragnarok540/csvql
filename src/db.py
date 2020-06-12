import sqlite3


def query_db(path, query, args=(), one=False):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(query, args)
    db.commit()
    rv = cur.fetchall()
    cur.close()
    db.close()
    return (rv[0] if rv else None) if one else rv


def read_sql(path):
    result = ''
    with open(path) as file:
        result = file.read()
    return result


def drop_table(path, name):
    sql = f"DROP TABLE IF EXISTS {name}"
    query_db(path, sql)


def table_sql(path, name):
    sql = """
          SELECT sql
            FROM sqlite_master
           WHERE name = ?
          """
    result = query_db(path, sql, args=(name,), one=True)
    return list(result)[0]


def tables(path):
    sql = """
          SELECT name
            FROM sqlite_master
           WHERE type = ?
          """
    result = query_db(path, sql, args=("table",))
    result_t = list(map(lambda x: " ".join(list(x)), result))
    return " ".join(result_t)
