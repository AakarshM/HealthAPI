import sqlite3
from flask import *
import bcrypt

conn = sqlite3.connect('./healthdb.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS nutrition (nutri TEXT, email TEXT PRIMARY KEY , '
            'pass TEXT, weight TEXT, height TEXT, age TEXT)')
conn.commit()

#nutri will be JSON