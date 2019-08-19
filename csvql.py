import argparse
import json
from lib import CSVRW, DB


def _exec(args):
    db = DB(args.connect)
    sql = args.sql_query
    if args.sql_file:
        sql = db.read_sql(args.sql_file)
    print(f"executing: '{sql}'") if args.verbose else None
    db.query_db(sql)
    db.close()


def _export(args):
    db = DB(args.connect)
    if args.verbose:
        print(f"connected to '{args.connect}'...")
    sql = args.sql_query
    if args.sql_file:
        sql = db.read_sql(args.sql_file)
    print(f"executing: '{sql}'...") if args.verbose else None
    result = db.query_db(sql)
    db.close()
    if args.format == "csv":
        if args.verbose:
            print(f"using delimiter: '{args.delimiter}'...")
            if args.header:
                print(f"generating header...")
        csvrw = CSVRW(args.file_name, args.delimiter)
        csvrw.write(result, args.header)
    elif args.format == "json":
        list = []
        for item in result:
            list.append(dict(zip(item.keys(), item)))
        with open(args.file_name, 'w') as json_file:
            json.dump(list, json_file, indent=2)
    if args.verbose:
        print(f"{args.file_name} created")
        print(f"{len(result)} rows written")


def _desc(args):
    db = DB(args.connect)
    for table in args.table_name:
        db.print_sql(table)
    db.close()


def _drop(args):
    db = DB(args.connect)
    for table in args.table_name:
        db.drop_table(table)
        print(f"{table} dropped") if not args.quiet else None
    db.close()


def _import(args):
    if args.verbose:
        print(f"connected to {args.connect}...")
        print(f"reading {args.file_name}...")
        print(f"using delimiter '{args.delimiter}'...")
        if args.header:
            print(f"generating header...")
        if args.ignore > 0:
            print(f"ignoring first {args.ignore} rows...")
    csvrw = CSVRW(args.file_name, args.delimiter)
    csv = csvrw.read(args.ignore)
    db = DB(args.connect)
    columns = db.columns(csv, args.header)
    types = db.types(csv, args.header)
    db.create_table(args.table_name, columns, types)
    db.bulk_insert(args.table_name, csv, args.header)
    db.close()
    if not args.quiet:
        print(f"{len(csv)} rows inserted into {args.table_name}")


def _query(args):
    db = DB(args.connect)
    sql = args.sql_query
    if args.sql_file:
        sql = db.read_sql(args.sql_file)
    print(f"executing: '{sql}'") if args.verbose else None
    result = db.query_db(sql)
    if args.all:
        db.print_table(result, header=args.header)
        print(f"{len(result)} rows in result") if not args.quiet else None
    else:
        db.print_table(result,
                       header=args.header,
                       maxr=args.num_rows)
        if not args.quiet:
            print(f"""{len(result)} rows in result""")
            if len(result) > args.num_rows:
                print(f"""{args.num_rows} rows shown""")
    db.close()


def _tables(args):
    db = DB(args.connect)
    db.print_tables()
    db.close()


parent_parser = argparse.ArgumentParser(add_help=False)

# Option Commands
parent_parser.add_argument("-c", "--connect", default="sqlite.db",
                           help="""create or connect to an SQLite
                                   database file, default is 'sqlite.db'""")
parent_parser.add_argument("-d", "--delimiter", default=",",
                           help="""assign a delimiter, default is ','""")
parent_parser.add_argument("-H", "--header", action="store_false",
                           help="""read a CSV file that has no header
                                   (generates column names), or write a
                                   CSV file with no header""")
parent_parser.add_argument("-s", "--sql-file",
                           help="""load query in a SQL file, overrides
                                   sql_query arguments for the 'export',
                                   'query' and 'exec' sub-commands""")

# Verbose and Quiet Group
group_v_q = parent_parser.add_mutually_exclusive_group()
group_v_q.add_argument("-v", "--verbose", action="store_true")
group_v_q.add_argument("-q", "--quiet", action="store_true")

parser = argparse.ArgumentParser(prog="csvql", parents=[parent_parser])

# Version
parser.add_argument("--version", action="version",
                    version="%(prog)s version 0.0.5",
                    help="""print version number on screen and exit""")

subparsers = parser.add_subparsers(help="""sub-command help""")

# Exec sub-command
parser_exec = subparsers.add_parser("exec",
                                   help="""execute an given SQL statement""")
parser_exec.add_argument("sql_query", help="""SQL statement""")
parser_exec.set_defaults(func=_exec)

# Export sub-command
parser_export = subparsers.add_parser("export",
                                      help="""write a file with the
                                              content of a query result""")
parser_export.add_argument("file_name",
                           help="""file to write""")
parser_export.add_argument("sql_query",
                           help="""select SQL statement""")
parser_export.add_argument("-f", "--format", default="csv",
                         help="""format of exported file, default is csv and
                                 json is supported""")
parser_export.set_defaults(func=_export)

# Desc sub-command
parser_desc = subparsers.add_parser("desc",
                                    help="""print the SQL create statement of
                                            the given table(s)""")
parser_desc.add_argument("table_name", nargs='*',
                         help="""name(s) of the table(s) to be described""")
parser_desc.set_defaults(func=_desc)

# Drop sub-command
parser_drop = subparsers.add_parser("drop",
                                    help="""delete table(s)""")
parser_drop.add_argument("table_name", nargs='*',
                         help="""name(s) of the table(s) to
                                 be deleted""")
parser_drop.set_defaults(func=_drop)

# Import sub-command
parser_import = subparsers.add_parser("import",
                                    help="""read a CSV file and import
                                            into the database""")
parser_import.add_argument("file_name",
                         help="""CSV file to read""")
parser_import.add_argument("table_name",
                         help="""name of the table to be created""")
parser_import.set_defaults(func=_import)

parser_import.add_argument("-i", "--ignore", type=int, default=0,
                         help="""ignore first n lines of the CSV file,
                                 default is 0""")

# Query sub-command
parser_query = subparsers.add_parser("query",
                                     help="""execute a query and print the
                                             result on the screen""")
parser_query.add_argument("sql_query",
                          help="""select SQL statement""")
parser_query.set_defaults(func=_query)

group_r_a = parser_query.add_mutually_exclusive_group()
group_r_a.add_argument("-r", "--num-rows", type=int, default=10,
                       help="""number of rows to print on screen,
                               default is 10""")
group_r_a.add_argument("-a", "--all", action="store_true",
                       help="""print all rows of the result""")

# Tables sub-command
parser_tables = subparsers.add_parser("tables",
                                      help="""print the names of all
                                              tables""")
parser_tables.set_defaults(func=_tables)

# Parse args and run function
args = parser.parse_args()
args.func(args)

def main():
    pass
