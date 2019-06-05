from csvrw import CSVRW
from db import DB

def main():
    csvrw = CSVRW('../data/csv_data.csv' , ',') 
    listt = csvrw.read()
    db = DB('../data/cars.db')
    columns = db.columns(listt)
    types = db.types(listt)
    print(db.create_table('CARS', columns, types))

if __name__ == '__main__':
    
    main()
