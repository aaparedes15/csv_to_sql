#!/usr/bin/env python

"""
Take an input file in csv format and 
create an SQL database table.
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


