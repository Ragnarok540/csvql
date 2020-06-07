import sys

def type_value(value):
    if value == "":
        return "NULL"
    try:
        int(value)
        return "INTEGER"
    except ValueError:
        try:
            float(value)
            return "REAL"
        except ValueError:
            return "TEXT"

def type_column(table, column):
    integer = False
    real = False
    text = False
    for row in table:
        type_c = type_value(row[column])
        if type_c == "INTEGER":
            integer = True
        elif type_c == "REAL":
            real = True
        elif type_c == "TEXT":
            text = True
    if text:
        return "TEXT"
    if real:
        return "REAL"
    if integer:
        return "INTEGER"
    return "TEXT"

def types(table, header=True):
    if header:
        table.pop(0)
    typs = []
    for column in range(0, len(table[0])):
        typs.append(type_column(table, column))
    return typs

def columns(table, file_header=True):
    cols = []
    header = table[0]
    counter = 0
    for column in header:
        if file_header:
            cols.append(column)
        else:
            cols.append(f"col_{counter}")
            counter = counter + 1
    return cols

def create_table(self, name, table, file_header=True):
    statement = []
    statement.append("CREATE TABLE")
    statement.append(name)
    statement.append("(")
    cols = columns(table, file_header)
    typs = types(table, file_header)
    col_types = list(zip(cols, typs))
    col_types = list(map(lambda x: " ".join(list(x)), col_types))
    statement.append(", ".join(col_types))
    statement.append(");")
    return " ".join(statement)

def bulk_insert(name, table, header=True):
    statement = []
    statement.append("INSERT INTO")
    statement.append(name)
    statement.append("VALUES")
    counter = 0
    for row in table:
        statement.append("(")
        for column in range(0, len(table[0])):
            type_c = type_value(row[column])
            if type_c == "NULL":
                statement.append("NULL")
            else:
                statement.append(f"'{row[column]}'")
            if column < (len(table[0]) - 1):
                statement.append(",")
        statement.append(")")
        if counter < (len(table) - 1):
            statement.append(",")
        counter = counter + 1
    statement.append(";")
    return " ".join(statement)

def print_table(table, header=True, maxr=sys.maxsize):
    if header:
        try:
            print(table[0].keys())
        except Exception:
            raise
    counter = 0
    for row in table:
        try:
            print(list(row))
        except Exception:
            raise
        counter = counter + 1
        if counter >= maxr:
            break
