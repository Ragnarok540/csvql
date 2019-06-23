import argparse
from csvrw import CSVRW
from db import DB

parser = argparse.ArgumentParser(prog='csvql')
parser.add_argument('command', choices=['query', 'table', 'list'],
                    help="choose command: query, table or list")
parser.add_argument('sql',
                    help="table name or SQL statement to evaluate (inside single or double quotes), can be an empty string")
group_v_q = parser.add_mutually_exclusive_group()
group_v_q.add_argument("-v", "--verbose", action="store_true")
group_v_q.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("-c", "--connect", default="sqlite.db",
                    help="create or connect to a database file, default is 'sqlite.db'")
parser.add_argument("-s", "--sql-file", default="",
                    help="load query in a SQL file for evaluation, overrides sql argument")
parser.add_argument("-d", "--delimiter", default=",",
                    help="assign delimiter, default is ','")
parser.add_argument("-H", "--header", action="store_false",
                    help="use to read a CSV file that has no header (generates column names), or to write a CSV file with no header")
parser.add_argument("-i", "--ignore", type=int, default=0,
                    help="ignore first n lines of a CSV file, default is 0")
parser.add_argument("-p", "--print", action="store_true",
                    help="print query result on screen")
group_r_a = parser.add_mutually_exclusive_group()
group_r_a.add_argument("-r", "--num-rows", type=int, default=10,
                    help="number of rows to print on screen, default is 10")
group_r_a.add_argument("-a", "--all", action="store_true",
                    help="print all rows of the result")
group = parser.add_mutually_exclusive_group()
group.add_argument("-l", "--load",
                   help="read a CSV file and load into the database")
group.add_argument("-u", "--unload",
                   help="write a CSV file with the content of a query result or a table")
group.add_argument("-D", "--drop", action="store_true",
                   help="drop a table")
group.add_argument("-e", "--describe", action="store_true",
                   help="print create sql")
parser.add_argument("--version", action='version', version='%(prog)s v0.0.1',
                    help="print version number on screen and exit")

args = parser.parse_args()

#Connect to database
db = DB(args.connect)
message = "" # str(args.load)

if args.command == 'table':
    if args.load:
        csvrw = CSVRW(args.load, args.delimiter)
        csv = csvrw.read()
        columns = db.columns(csv)
        types = db.types(csv, args.header)
        db.create_table(args.sql, columns, types)
        db.bulk_insert(args.sql, csv, args.header)
    elif args.describe:
        db.print_sql(args.sql)
    elif args.drop:
        db.drop_table(args.sql)
elif args.command == 'list':
    db.print_tables()
elif args.command == 'query':
    result = db.query_db(args.sql)
    if args.unload:
        csvrw = CSVRW(args.unload, args.delimiter)
        csvrw.write(result, args.header)
    if args.print:
        try:
            if args.all:
                db.print_table(result, header=args.header)
            else:
                db.print_table(result, header=args.header, maxr=args.num_rows)
        except:
            print("No results!")

if args.quiet:
    print("")
elif args.verbose:
    print(f"database: {message}")
else:
    print(f"{message}")
