import sqlite3 as lite
import sys
connect = None


connect = lite.connect('test.db')
cur = connect.cursor()
sqlite_select_query = """SELECT city, prof, sallary_from, sallary_to from hhotelka"""
cur.execute(sqlite_select_query)
records = cur.fetchall()

print(len(records))

for row in records:
    print(row)

connect = lite.connect('test.db')
cur = connect.cursor()
sqlite_select_query = """SELECT city, prof, sallary_from, sallary_to from hh"""
cur.execute(sqlite_select_query)
records = cur.fetchall()

print(len(records))

for row in records:
    print(row)