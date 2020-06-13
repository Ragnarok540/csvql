import unittest
import sqlite3
from os import unlink
from os.path import join, dirname, realpath, isfile
from src.csvrw import read, write
from src.db import query_db


class CSVRWTest(unittest.TestCase):

    def setUp(self):
        self.expected = [['test1', 'test2', 'test3'], ['1', '2', '3'], ['4', '5', '6']]
        self.read_path = join(dirname(realpath(__file__)), 'csv/read.csv')
        self.read_delim_path = join(dirname(realpath(__file__)), 'csv/read_delim.csv')
        self.read_ignore_path = join(dirname(realpath(__file__)), 'csv/read_ignore.csv')
        self.write_path = join(dirname(realpath(__file__)), 'csv/write.csv')

    def tearDown(self):
        if isfile(self.write_path):
            unlink(self.write_path)

    def write_helper(self):
        db = sqlite3.connect(':memory:')
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.executescript("""
            CREATE TABLE temp (test1 INTEGER, test2 INTEGER, test3 INTEGER);
            INSERT INTO temp VALUES ('1', '2', '3'), ('4' ,'5' ,'6');
            """)
        db.commit()
        cur.execute('SELECT * FROM temp', ())
        rv = cur.fetchall()
        cur.close()
        db.close()
        return rv

    def test_read(self):
        observed = read(self.read_path)
        self.assertEqual(self.expected, observed)

        observed = read(self.read_delim_path, delim=';')
        self.assertEqual(self.expected, observed)

        observed = read(self.read_ignore_path, ignore=2)
        self.assertEqual(self.expected, observed)

    def test_write(self):
        table = self.write_helper()
        write(self.write_path, table)
        observed = read(self.write_path)
        self.assertEqual(self.expected, observed)

    def test_write_delim(self):
        table = self.write_helper()
        write(self.write_path, table, delim='$')
        observed = read(self.write_path, delim='$')
        self.assertEqual(self.expected, observed)

    def test_write_header(self):
        table = self.write_helper()
        write(self.write_path, table, header=False)
        observed = read(self.write_path)
        self.assertEqual(self.expected[1:], observed)
