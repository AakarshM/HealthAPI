from flask import *
import bcrypt
import sqlite3
import json
import models.doctor as doctor
from validate_email import validate_email
import models.patient as patient
import models.nutrition as nutrition
import models.points as points


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?.RT'


@app.route('/')
def index():
    return "root view"

@app.route('/create-patient', methods=['POST'])
def createpatientfront():
    user_data = request.get_json()
    email = user_data['email']
    name = user_data['name']
    password = user_data['password']
    weight = user_data['weight']
    height = user_data['height']
    gender = user_data['gender']
    age = user_data['age']
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    print(hashed_password)
    try:
        patient.create(name, email, hashed_password, weight, height, age, gender)
        return "safe"
    except sqlite3.Error as error:
        if 'UNIQUE constraint failed' in str(error):
            return "User exists"
        else:
            return "User with email " + email + " created"


@app.route('/create-doctor', methods=['POST'])
def createdocfront():
    doc_data = request.get_json()
    email = doc_data['email']
    password = doc_data['password']
    name = doc_data['name']
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    doctor.create(name, email, hashed_password)
    return "done"


@app.route('/add-patient', methods=['POST'])
def addpatientdoc():
    user_data = request.get_json()
    email = user_data['email']
    name = user_data['name']
    weight = user_data['weight']
    height = user_data['height']
    gender = user_data['gender']
    age = user_data['age']
    calories_intake = user_data['calories intake']
    calories_exercise = user_data['calories exercise']
    protein = user_data['protein']
    carbs = user_data['carbs']
    fats = user_data['fats']
    doctor.addpatient(email, name, age, weight, height, calories_exercise, calories_intake, protein, carbs, fats, gender)
    #email, name, age, weight, height, calories_exercise, calories_intake, protein, carbs, fats, gender
    return "Added patient: " + email

@app.route('/edit-patient', methods=['PATCH'])
def editpatientdoc():
    if 'auth' not in session:
        abort(401)
    else:
     user_data = request.get_json()
     email = user_data['email']
     calories_intake = user_data['calories intake']
     calories_exercise = user_data['calories exercise']
     protein = user_data['protein']
     carbs = user_data['carbs']
     fats = user_data['fats']
     edited_patient = doctor.editpatient(email, calories_exercise, calories_intake, protein, carbs, fats)
     return edited_patient
#email, calories_exercise, calories_intake, protein, carbs, fats)

@app.route('/common-goal')
def method():
   return "none"

@app.route('/login-patient', methods=['POST'])
def login():
    user_data = request.get_json()
    email = user_data['email']
    password = user_data['password']
    login = patient.login(email, password.encode('utf-8'))
    if(login == None):
        return "No user exists"
    elif(login == "WrongPass"):
        return "Wrong password"
    else:
        session['auth'] = email
        return "logged in"

@app.route('/get-patient-data', methods=['GET'])
def fetch_patient():
    if 'auth' not in session:
        abort(401)
    else:
        patient_info = patient.fetchdata()
        return patient_info


@app.route('/login-doctor', methods=['POST'])
def logindoctor():
    user_data = request.get_json()
    email = user_data['email']
    password = user_data['password']
    login = doctor.login(email, password.encode('utf-8'))
    if (login == None):
        return "No user exists"
    elif (login == "WrongPass"):
        return "Wrong password"
    else:
        session['auth'] = email
        return "logged in"


@app.route('/get-points', methods=['GET'])
def retrivepoints():
    data_points = points.getdatatable()
    return data_points

if __name__ == "__main__":
    app.run()
