# CSV-SQL
CSV-SQL is an easy to use, open source command line tool to
work with CSV files.

# Features
- Load one or more CSV files into an embedded database as tables
- Query the data using SQL
- Create new CSV files from the result of an SQL query

## Commands

These are a few examples of how the aplication is used.

### load

To load a file into the database use 'load': 

```sh
(csv-sql) load csv_data.csv cars
```

### tables

To see what tables are currently loaded use 'tables':

```sh
(csv-sql) tables
cars
```

### desc

To see the DDL statement CSV-SQL used to create the table use 'desc':

```sh
(csv-sql) desc cars
CREATE TABLE cars ( year INTEGER, make TEXT, model TEXT )
```

### query

To apply an SQL query use 'query':

```sh
(csv-sql) query select year, count(*) as count from cars where make = 'BMW' group by year order by count desc
15 result(s).
```

### last

To see the results of the last SQL query use 'last':

```sh
(csv-sql) last
['year', 'count']
[2014, 86]
[2015, 77]
[2013, 71]
[2012, 60]
```

### unload

To write a new CSV file from the results of the last SQL query
use 'unload':

```sh
(csv-sql) unload bmw.csv
```

Uses:

- https://github.com/arthurkao/vehicle-make-model-data
