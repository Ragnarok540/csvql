from csvrw import CSVRW
from db import DB

def main():
    csvrw = CSVRW('../data/csv_data.csv', ',', '"')
    list = csvrw.read()
    #print(list)
    db = DB('../data/cars.db')
    db.create_table('baz', ['foo', 'bar'], ['int', 'text']);

if __name__ == '__main__':
    
    main()
