#!/bin/bash
# CSV file importing example

# Read file and import data into table
csvql --verbose import shops.csv shop

# Describe table
csvql desc shop

# Query table and show results
csvql --verbose query "select * from shop"

# Drop table
csvql drop shop
