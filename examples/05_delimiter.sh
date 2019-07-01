#!/bin/bash
# CSV file custom delimiter example

# Read file and import data into table
csvql -d ";" import shops_d.csv shop

# Query table and write file
csvql -d "@" -v export shops3.csv "select * from shop where id % 2 = 0"

# Drop table
csvql drop shop
