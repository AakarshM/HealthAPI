import sqlite3
from flask import *
import bcrypt

conn = sqlite3.connect('./healthdb.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS patients (name TEXT, email TEXT PRIMARY KEY, '
            'pass TEXT, weight TEXT, height TEXT, age TEXT, gender TEXT, doctor TEXT)')
conn.commit()

default_doc = ""

#creates the patient
def create(name, email, hash, weight, height, age, gender):
        cur.execute('INSERT INTO patients VALUES (?,?,?,?,?,?,?,?)', (name, email, hash, weight, height, age, gender,
                                                                      default_doc))
        conn.commit()


def login(email, password):
     cur.execute('SELECT pass FROM patients WHERE email=(?)', (email,))
     hash_check = cur.fetchone()
     if hash_check == None:
         return None
     else:
        hashed_password = hash_check[0]
        print(hashed_password)
        if bcrypt.checkpw(password, hashed_password):
            session['auth'] = email
            return "Log"
        else:
            return "WrongPass"

def fetchdata():
    patient_email = session['auth']
    cur.execute('SELECT doctor FROM patients WHERE email=(?)', (patient_email,))
    doc = cur.fetchone()[0]
    print(doc)
    cur.execute('SELECT patients FROM doctors WHERE email=(?)', (doc,))
    patients = cur.fetchone()[0]
    patients_json = json.loads(patients)
    current_patient = patients_json[patient_email]
    current_patient_text = json.dumps(current_patient)
    return current_patient_text #all of patient data