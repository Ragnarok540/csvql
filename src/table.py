import sys


def type_value(value) -> str:
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


def type_column(table: list, column: int) -> str:
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


def types(table: list, header: bool = True) -> list[str]:
    if header:
        table.pop(0)
    typs = []
    for column in range(0, len(table[0])):
        typs.append(type_column(table, column))
    return typs


def columns(table: list, header: bool = True):
    cols = []
    table_header = table[0]
    counter = 0
    for column in table_header:
        if header:
            cols.append(column)
        else:
            cols.append(f"col_{counter}")
            counter = counter + 1
    return cols


def create_table(name: str, table: list, header: bool = True):
    statement = []
    statement.append("CREATE TABLE")
    statement.append(name)
    statement.append("(")
    cols = columns(table, header)
    typs = types(table, header)
    col_types = list(zip(cols, typs))
    col_types = list(map(lambda x: " ".join(list(x)), col_types))
    statement.append(", ".join(col_types))
    statement.append(");")
    return " ".join(statement)


def bulk_insert(name: str, table: list, header: bool = True):
    if header:
        table.pop(0)
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


def print_table(table: list, header: bool = True, maxr: int = sys.maxsize):
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
