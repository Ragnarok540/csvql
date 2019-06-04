import csv

class CSVRW:
    def __init__(self, path, delimiter, quotechar):
        self.path = path
        self.delimiter = delimiter
        self.quotechar = quotechar

    def read(self):
        list = []
        with open(self.path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter, quotechar=self.quotechar)
            for row in reader:
                list.append(row)
        return list
