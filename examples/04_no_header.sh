#!/bin/bash
# CSV file with no header example

# Read file and import data into table
csvql -H import shops_nh.csv shop

# Describe tables
csvql desc shop

# Query and show results
csvql query "select * from shop"

# Drop tables
csvql drop shop
