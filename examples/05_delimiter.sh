#!/bin/bash
# CSV file custom delimiter example

# Read file and import data into table
csvql --verbose --delimiter ";" import shops_d.csv shop

# Query table and write file
csvql --verbose --delimiter "@" export shops3.csv "select * from shop where id % 2 = 0"

# Drop table
csvql drop shop
