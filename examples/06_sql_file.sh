#!/bin/bash
# SQL file query example

# Read files and import data into tables
csvql --verbose import shops.csv shop
csvql --verbose import products.csv product

# Print table names
csvql tables

# Describe tables
csvql desc shop product

# Query and show results
csvql --sql-file query_count.sql query ""

# Drop tables
csvql drop shop product
