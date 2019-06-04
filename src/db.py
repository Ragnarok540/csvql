import sqlite3

class DB:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row

    def query_db(self, query, args=(), one=False):
        cur = self.db.cursor()
        cur.execute(query, args)
        self.db.commit()
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

    def close(self):
        self.db.close()

    def create_table(self, name, columns, types):
        statement = []
        statement.append("CREATE TABLE")
        statement.append(name)
        statement.append("(")
        colums_types = list(zip(columns, types))
        print(colums_types)
        colums_types = list(map(lambda x: ' '.join(list(x)), colums_types))
        print(colums_types)
        statement.append(', '.join(colums_types))
        statement.append(")")
        print(' '.join(statement))
        #self.query_db(' '.join(statement))
