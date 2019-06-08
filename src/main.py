from csvrw import CSVRW
from db import DB

def main():
##    csvrw = CSVRW('../data/csv_data.csv', ',') 
##    csv = csvrw.read()
      db = DB('../data/cars.db')
##    columns = db.columns(csv)
##    types = db.types(csv)
##    sql_create = db.create_table('CARS', columns, types)
##    db.query_db(sql_create)
##    sql_insert = db.bulk_insert('CARS', csv)
##    db.query_db(sql_insert)
      #result = db.query_db("select year, make, count(*) from CARS group by year, make")
      #print(result[0].keys())
      #print(list(result[0]))
      #csvrw = CSVRW('../data/csv_result.csv', ';')
      #csvrw.write(result)
      #db.print_table(result)
      #db.print_sql('CARS')
      db.drop_table('CARS');

if __name__ == '__main__':
    
    main()
