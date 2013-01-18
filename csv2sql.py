#!/usr/bin/env python

"""
Take an input file in csv format and 
create an SQL database table.

To run from the command line:
    csv2sql.py "csv_file_name"
"""

# import needed modules
import sqlite3
from   matplotlib.mlab import csv2rec

# get csv file from command line
from sys import argv
csv_file = argv[1]

# Get the arguments from the command
# line for the csv2sql command.
from optparse import OptionParser

# set the options
parser = OptionParser()
parsser.add_option("-h", "--help", action="help")
parser.add_option("--database", dest="database", default=csv_file[:-4],
                  help="Specify output database.", metavar="DATABASE")
parser.add_option("-t", "--table", dest="table", default=csv_file[:-4]
                  help="Specify output table.", metavar="TABLE")
parser.add_option("-c", "--comments", dest="comments", default="#",
                  help="Specify symbol which signifies comment lines.",
                  metavar="COMMENT")
parser.add_option("-d", "--delimiter", dest="delimiter", default=",",
                  help="Specify delimiter of csv file data.", 
                  metavar="DELIMITER")
# put optional args in a dict
opts = {'database':database, 
        'table':table, 
        'comment':comment, 
        'delimiter':delimiter}

def get_data_type(data):
    """
    Get the data type of 
    the input and return
    the SQL data type name.
    """
    
    if "string" in str(type(data)): return "TEXT"
    if "float"  in str(type(data)): return "REAL"
    if "int"    in str(type(data)): return "INTEGER"

def csv2sql(database, table, comments="#", delimiter=","):
    """
    The main method that will
    take in the csv file and 
    create a database and
    a table.
    """
    global csv_file

    # create the database and cursor
    con = sqlite3.connect(database)
    cur = con.cursor()

    # load in the data
    data = csv2rec(csv_file, comments=comments, delimiter=delimiter)

    # make the table
    create_table_command = "CREATE TABLE {0} (".format(table)
    for n, t in zip(data.dtype.names, data[0]):
        create_table_command += "{0} {1}, ".format(n, get_data_type(t))
    create_table_command += ")"
    cur.execute(create_table_command)

    # insert the rows of data into the table.
    for row in data:
        cur.execute(
            "INSERT INTO {0} VALUES {1}".format(table, str(row)))

    # Save (commit) the database
    con.commit()

    # close the connection to the database
    con.close()


# To run it from command line
if __name__=="__main__":
    # get optional arguments from command line
    args = get_args()
    csv2sql(opts['database'], 
            opts['table'], 
            comments=opts['comments'], 
            delimiter=opts['delimiter'])
