import sqlite3
from flask import *
import bcrypt

conn = sqlite3.connect('./healthdb.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS points (name TEXT, email TEXT PRIMARY KEY, '
            'points INTEGER)')
conn.commit()

def getdatatable():
    cur.execute('SELECT * FROM points ORDER BY points DESC')
    table = cur.fetchall()
    lst = []
    for item in table:
        lst.append({"name": item[0],
                    "points" : item[2]})
    j = json.dumps(lst)
    return j