#!/bin/bash
# CSV file exporting example

# Read file and import data into table
csvql import shops.csv shop

# Query table and write file
csvql -v export shops2.csv "select * from shop where id in (1, 2)"

# Drop table
csvql drop shop
