from csv import reader, writer


def read(path: str, delim: str = ',', ignore: int = 0) -> list:
    result = []
    with open(path, newline='') as csv_file:
        csv_reader = reader(csv_file, delimiter=delim)
        counter = 0
        for row in csv_reader:
            if counter < ignore:
                counter = counter + 1
                continue
            result.append(row)
    return result


def write(path: str, table: list, delim: str = ',', header: bool = True) -> None:
    with open(path, mode='w', newline='') as csv_file:
        csv_writer = writer(csv_file, delimiter=delim)
        if header:
            csv_writer.writerow(table[0].keys())
        for row in table:
            csv_writer.writerow(row)
