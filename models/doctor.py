import sqlite3
from flask import *
import bcrypt

conn = sqlite3.connect('./healthdb.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS doctors (email TEXT PRIMARY KEY, pass TEXT, name TEXT, patients TEXT)')
conn.commit()

#patients will be JSON

default_patients = str({})
"""
patient (email): {
name: x
age: x,
weight: x,
height: x,
calories exercise: x
calories intake: x,
macros: {protein: x, carbs: x, fats: x, fiber: x}
}

"""
def create(name, email, hash):
    cur.execute('INSERT INTO doctors VALUES (?,?,?,?)', (email, hash, name, default_patients))
    conn.commit()


def login(email, password):
    cur.execute('SELECT pass FROM doctors WHERE email=(?)', (email,))
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


def addpatient(email, name, age, weight, height, calories_exercise, calories_intake, protein, carbs, fats, gender):
    doc_email = session['auth']
    cur.execute('SELECT patients FROM doctors where email=(?)', (doc_email,))
    conn.commit()
    selected_patients = cur.fetchone()[0]
    selected_patients_json = json.loads(selected_patients)
    patient_json = {"name": name,
                    "age": age,
                    "weight": weight,
                    "height": height,
                    "gender": gender,
                    "calories exercise": calories_exercise,
                    "calories intake": calories_intake,
                    "macros": {
                        "protein": protein,
                        "carbs": carbs,
                        "fats": fats
                    }}
    selected_patients_json[email] = patient_json
    print(selected_patients_json)
    new_patients_json = json.dumps(selected_patients_json)
    cur.execute('UPDATE doctors SET patients =(?) WHERE email=(?)', (new_patients_json, doc_email,))
    conn.commit()
    adddoctopatient(email)


def adddoctopatient(email): #email is the patient email
    doc_email = session['auth']
    try:
        cur.execute('SELECT doctor from patients WHERE email=(?)', (email,))
    except sqlite3.Error as error:
        return "Error"
    else:
        doc_field = cur.fetchone()[0]
        cur.execute('UPDATE patients SET doctor =(?) WHERE email=(?)', (doc_email, email))

def editpatient(email, calories_exercise, calories_intake, protein, carbs, fats):
    doc_email = session['auth']
    try:
        cur.execute('SELECT patients FROM doctors where email=(?)', (doc_email, ))
    except sqlite3.Error as error:
        print(error)
        return str(error)
    else:
        patients_text = cur.fetchone()[0]
        patients_json = json.loads(patients_text) #all patients
        specific_patient = patients_json[email]
        specific_patient['calories_exercise'] = calories_exercise
        specific_patient['calories_intake'] = calories_intake
        patient_macros = specific_patient['macros']
        patient_macros['carbs'] = carbs
        patient_macros['protein'] = protein
        patient_macros['fats'] = fats
        new_patient_text = json.dumps(patients_json)
        cur.execute('UPDATE doctors set patients =(?) WHERE email=(?)', (new_patient_text, doc_email))
        conn.commit()
        return new_patient_text

