#!/bin/bash
# CSV file exporting example

# Read file and import data into table
csvql --verbose import shops.csv shop

# Query table and write file
csvql --verbose export shops2.csv "select * from shop where id in (1, 2)"

# Drop table
csvql drop shop
