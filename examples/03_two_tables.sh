#!/bin/bash
# two or more CSV files example

# Read files and import data into tables
csvql import shops.csv shop
csvql import products.csv product

# Print table names
csvql tables

# Describe tables
csvql desc shop product

# Query and show results
csvql query "select s.name as shop,
                    p.name as product,
                    p.price
               from shop s,
                    product p
              where s.id = p.shop_id
           order by p.price desc"

# Drop tables
csvql drop shop product
