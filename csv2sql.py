#!/usr/bin/env python

"""
Take an input file in csv format and 
create an SQL database table.

To run from the command line:
    csv2sql.py "csv_file_name"
"""

import sqlite3
from   matplotlib.mlab import csv2rec

def get_data_type(data):
    """
    Get the data type of 
    the input and return
    the SQL data type name.
    """
    
    if "string" in str(type(data)): return "TEXT"
    if "float"  in str(type(data)): return "REAL"
    if "int"    in str(type(data)): return "INTEGER"

def main(csv_file):
    """
    The main method that will
    take in the csv file and 
    create a database and
    a table.
    """

    # create the database name as same name
    # as csv file with .db extension instead of
    # .csv extension.
    database =  csv_file[:-4] + ".db"

    # create the database and cursor
    con = sqlite3.connect(database)
    cur = con.cursor()

    # load in the data
    data = csv2rec(csv_file)

    # make the table
    create_table_command = "CREATE TABLE {0} (".format(csv_file[:-4])
    for n, t in zip(data.dtype.names, data[0]):
        create_table_command += "{0} {1}, ".format(n, get_data_type(t))
    create_table_command += ")"
    cur.execute(create_table_command)

    # insert the rows of data into the table.
    for row in data:
        cur.execute(
            "INSERT INTO {0} VALUES {1}".format(csv_file[:-4],str(row)))

    # Save (commit) the database
    con.commit()

    # close the connection to the database
    con.close()

# To run it from command line
if __name__=="__main__":
    from sys import argv
    main(argv[1])
