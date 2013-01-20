#!/usr/bin/env python

"""
Take an input file in csv format and 
create an SQL database table.

To run from the command line:
    csv2sql.py "csv_file_name" [options]
"""

# import needed modules
import sqlite3

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
    
    if type(data) == str: return "TEXT"
    if type(data) == int: return "INTEGER"
    if type(data) == float: return "REAL"

def import_data(file, comments="#", delimiter=","):
    """
    Put the data into a list
    of list, ommitting comment
    lines.
    """
    data = open(file) 
    rows = []
    for row in data.readlines():
        if row[0] == comments: pass
        rows.append(row.split(delimiter)[:-1])
    return rows

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
    data = import_data(csv_file, comments=comments, delimiter=delimiter)

    # make the table
    create_table_command = "CREATE TABLE {0} (".format(table)
    for n in data[0]:
        create_table_command += "{0} {1}, ".format(n, get_data_type(n))
    create_table_command += ")"
    cur.execute(create_table_command)

    # insert the rows of data into the table.
    for row in data[1:] 
        cur.execute(
            "INSERT INTO {0} VALUES {1}".format(table, str(tuple(row))))

    # Save (commit) the database
    con.commit()

    # close the connection to the database
    con.close()


# To run it from command line
if __name__=="__main__":
    csv2sql(opts['database'], 
            opts['table'], 
            comments=opts['comments'], 
            delimiter=opts['delimiter'])
