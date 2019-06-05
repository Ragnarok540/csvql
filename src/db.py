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
        columns_types = list(zip(columns, types))
        columns_types = list(map(lambda x: ' '.join(list(x)), columns_types))
        statement.append(', '.join(columns_types))
        statement.append(")")
        print(' '.join(statement))
        #self.query_db(' '.join(statement))

    def type_value(self, value):
        if value == "":
            return "NULL"
        try:
            int(value)
            return "INTEGER"
        except:
            try:
                float(value)
                return "REAL"
            except:
                return "TEXT"

    def type_column(self, table, column):
        integer = False
        real = False
        text = False

        for row in table:
            type_c = self.type_value(row[column])
            if type_c == 'INTEGER':
                integer = True
            elif type_c == 'REAL':
                real = True
            elif type_c == 'TEXT':
                text = True

        if text == True:
            return "TEXT"
        if real == True:
            return "REAL"
        if integer == True:
            return "INTEGER"
        return "TEXT"

    def types(self, table):
        table.pop(0) # header
        types = []
        for column in range(0, len(table[0])):
            types.append(self.type_column(table, column))
        return types

    def columns(self, table):
        columns = []
        header = table[0]
        for column in header:
            columns.append(column)
        return columns
