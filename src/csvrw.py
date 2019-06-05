import csv

class CSVRW:
    def __init__(self, path, delimiter):
        self.path = path
        self.delimiter = delimiter

    def read(self):
        list = []
        with open(self.path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter )
            for row in reader:
                list.append(row)
        return list
