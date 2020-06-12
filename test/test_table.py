import unittest
from src.table import type_value, type_column, types, columns, create_table, bulk_insert


class TableTest(unittest.TestCase):

    def setUp(self):
        self.data = [["1",   "2",   "3", ""], 
                     ["4", "5.5", "6.6", ""], 
                     ["7",   "8",   "A", ""],
                     [ "",    "",    "", ""]]

        self.data_h = [["a",  "bc", "1", "23"], 
                       ["1", "5.5", "A",   ""]]

    def test_type_value(self):
        expected = "NULL"
        observed = type_value("")
        self.assertEqual(expected, observed)
        
        expected = "INTEGER"
        observed = type_value("123")
        self.assertEqual(expected, observed)
        
        expected = "REAL"
        observed = type_value("123.123")
        self.assertEqual(expected, observed)
        
        expected = "TEXT"
        observed = type_value("HELLO")
        self.assertEqual(expected, observed)
        
    def test_type_column(self):
        expected = "INTEGER"
        observed = type_column(self.data, 0)
        self.assertEqual(expected, observed)
        
        expected = "REAL"
        observed = type_column(self.data, 1)
        self.assertEqual(expected, observed)
        
        expected = "TEXT"
        observed = type_column(self.data, 2)
        self.assertEqual(expected, observed)
        
        expected = "TEXT"
        observed = type_column(self.data, 3)
        self.assertEqual(expected, observed)

    def test_types(self):
        expected = ['INTEGER', 'REAL', 'TEXT', 'TEXT']
        observed = types(self.data, header=False)
        self.assertEqual(expected, observed)

        expected = ['INTEGER', 'REAL', 'TEXT', 'TEXT']
        observed = types(self.data_h)
        self.assertEqual(expected, observed)

    def test_columns(self):
        expected = ['col_0', 'col_1', 'col_2', 'col_3']
        observed = columns(self.data, header=False)
        self.assertEqual(expected, observed)

        expected = ['a', 'bc', '1', '23']
        observed = columns(self.data_h)
        self.assertEqual(expected, observed)

    def test_create_table(self):
        expected = "CREATE TABLE data ( col_0 INTEGER, col_1 REAL, col_2 TEXT, col_3 TEXT );"
        observed = create_table("data", self.data, header=False)
        self.assertEqual(expected, observed)

        expected = "CREATE TABLE data_h ( a INTEGER, bc REAL, 1 TEXT, 23 TEXT );"
        observed = create_table("data_h", self.data_h)
        self.assertEqual(expected, observed)

    def test_bulk_insert(self):
        expected = "INSERT INTO data VALUES ( '1' , '2' , '3' , NULL ) , ( '4' , '5.5' , '6.6' , NULL ) , ( '7' , '8' , 'A' , NULL ) , ( NULL , NULL , NULL , NULL ) ;"
        observed = bulk_insert("data", self.data, header=False)
        self.assertEqual(expected, observed)

        expected = "INSERT INTO data_h VALUES ( '1' , '5.5' , 'A' , NULL ) ;"
        observed = bulk_insert("data_h", self.data_h)
        self.assertEqual(expected, observed)
