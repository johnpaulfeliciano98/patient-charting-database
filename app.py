from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
from database import db_connector as db

app = Flask(__name__)

# Configuration for MySQL database connection
app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''  # last 4 of ONID
app.config['MYSQL_DB'] = ''
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

# Establish database connection
db_connection = db.connect_to_database()
mysql = MySQL(app)

# Home route for testing MySQL connection
# @app.route('/')
# def root():
#     query1 = 'DROP TABLE IF EXISTS diagnostic;'
#     query2 = 'CREATE TABLE diagnostic(id INT PRIMARY KEY AUTO_INCREMENT, text VARCHAR(255) NOT NULL);'
#     query3 = 'INSERT INTO diagnostic (text) VALUES ("MySQL is working for 113!")'
#     query4 = 'SELECT * FROM diagnostic;'
#     cur = mysql.connection.cursor()
#     cur.execute(query1)
#     cur.execute(query2)
#     cur.execute(query3)
#     cur.execute(query4)
#     results = cur.fetchall()

#     return render_template("main.j2")

# This route is adapted from the CS 340 starter app
@app.route('/clinics')
def clinics():
    query = "SELECT * FROM Clinics;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    print(results)
    return render_template('clinics.j2', clinics=results)

# Route to add a new clinic, handles both GET and POST requests
@app.route('/add_clinic', methods=['POST', 'GET'])
def add_clinic():
    if request.method == "GET":
        query = "SELECT * FROM Clinics;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        print(results)
        return render_template('clinics.j2', clinics=results)

    if request.method == "POST":
        if request.form.get("addClinic"):
            clinic_name = request.form['clinic_name']
            address = request.form['address']
            phone_number = request.form['phone_number']
            email = request.form['email']

            print(f"Received data: {clinic_name}, {
                  address}, {phone_number}, {email}")

            query = """
            INSERT INTO Clinics (clinic_name, address, clinic_phone_number, email)
            VALUES (%s, %s, %s, %s)
            """

            cur = mysql.connection.cursor()
            cur.execute(query, (clinic_name, address, phone_number, email))
            mysql.connection.commit()

            return redirect("/clinics")

# Route to delete a clinic by ID
@app.route("/delete_clinics/<int:id>")
def delete_clinics(id):
    query = "DELETE FROM Clinics WHERE clinic_ID = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    return redirect("/clinics")

# Route to edit clinic details
@app.route("/edit_clinic", methods=["POST"])
def edit_clinic():
    if request.method == "POST":
        clinic_ID = request.form['clinic_ID']
        clinic_name = request.form['clinic_name']
        address = request.form['address']
        clinic_phone_number = request.form['clinic_phone_number']
        email = request.form['email']

        query = """
        UPDATE Clinics 
        SET clinic_name = %s, address = %s, clinic_phone_number = %s, email = %s
        WHERE clinic_ID = %s
        """

        cur = mysql.connection.cursor()
        cur.execute(query, (clinic_name, address,
                    clinic_phone_number, email, clinic_ID))
        mysql.connection.commit()

        return redirect("/clinics")

# Route to manage patients, handles both GET (read) and POST (create)
@app.route('/patients', methods=['POST', 'GET'])
def patients():
    if request.method == "GET":
        query = "SELECT * FROM Patients;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        # Fetch clinic IDs
        clinics_query = "SELECT clinic_ID FROM Clinics;"
        clinics_cursor = db.execute_query(
            db_connection=db_connection, query=clinics_query)
        clinics_results = clinics_cursor.fetchall()

        # Fetch procedure IDs
        procedures_query = "SELECT procedure_ID FROM Procedures;"
        procedures_cursor = db.execute_query(
            db_connection=db_connection, query=procedures_query)
        procedures_results = procedures_cursor.fetchall()

        return render_template('patients.j2', patients=results, clinics=clinics_results, procedures=procedures_results)

    if request.method == "POST":
        if request.form.get("addPatient"):
            patient_name = request.form['patient_name']
            date_of_birth = request.form['date_of_birth']
            patient_phone_number = request.form['patient_phone_number']
            clinic_ID = request.form['clinic_ID']
            procedure_ID = request.form['procedure_ID']

            query = """
            INSERT INTO Patients (patient_name, date_of_birth, patient_phone_number, clinic_ID, procedure_ID)
            VALUES (%s, %s, %s, %s, %s)
            """

            cur = mysql.connection.cursor()
            cur.execute(query, (patient_name, date_of_birth,
                        patient_phone_number, clinic_ID, procedure_ID))
            mysql.connection.commit()

            return redirect("/patients")

# Route to delete a patient by ID
@app.route("/delete_patient/<int:id>")
def delete_patient(id):
    query = "DELETE FROM Patients WHERE patient_ID = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    return redirect("/patients")

# Route to edit patient details
@app.route("/edit_patient", methods=["POST"])
def edit_patient():
    if request.method == "POST":
        patient_ID = request.form['patient_ID']
        patient_name = request.form['patient_name']
        date_of_birth = request.form['date_of_birth']
        patient_phone_number = request.form['patient_phone_number']
        clinic_ID = request.form['clinic_ID']
        procedure_ID = request.form['procedure_ID']

        query = """
        UPDATE Patients
        SET patient_name = %s, date_of_birth = %s, patient_phone_number = %s, clinic_ID = %s, procedure_ID = %s
        WHERE patient_ID = %s
        """

        cur = mysql.connection.cursor()
        cur.execute(query, (patient_name, date_of_birth,
                    patient_phone_number, clinic_ID, procedure_ID, patient_ID))
        mysql.connection.commit()

        return redirect("/patients")

# Route to manage doctors, handles both GET (read) and POST (create)
@app.route('/doctors', methods=['POST', 'GET'])
def doctors():
    if request.method == "GET":
        query = "SELECT * FROM Doctors;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        # Fetch clinic IDs
        clinics_query = "SELECT clinic_ID FROM Clinics;"
        clinics_cursor = db.execute_query(
            db_connection=db_connection, query=clinics_query)
        clinics_results = clinics_cursor.fetchall()

        print(results)
        return render_template('doctors.j2', doctors=results, clinics=clinics_results)

    if request.method == "POST":
        if request.form.get("addDoctor"):
            doctor_ID = request.form['doctor_ID']
            doctor_name = request.form['doctor_name']
            clinic_ID = request.form['clinic_ID']

            print(f"Received data: {doctor_ID}, {doctor_name}, {clinic_ID}")

            query = """
            INSERT INTO Doctors (doctor_ID, doctor_name, clinic_ID)
            VALUES (%s, %s, %s)
            """

            cur = mysql.connection.cursor()
            cur.execute(query, (doctor_ID, doctor_name, clinic_ID))
            mysql.connection.commit()

            return redirect("/doctors")

# Route to delete a doctor by ID
@app.route("/delete_doctors/<int:id>")
def delete_doctors(id):
    query = "DELETE FROM Doctors WHERE doctor_ID = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    return redirect("/doctors")

# Route to edit doctor details
@app.route("/edit_doctor", methods=["POST"])
def edit_doctor():
    if request.method == "POST":
        doctor_ID = request.form['doctor_ID']
        doctor_name = request.form['doctor_name']
        clinic_ID = request.form['clinic_ID']

        query = """
        UPDATE Doctors
        SET doctor_name = %s, clinic_ID = %s
        WHERE doctor_ID = %s
        """

        cur = mysql.connection.cursor()
        cur.execute(query, (doctor_name, clinic_ID, doctor_ID))
        mysql.connection.commit()

        return redirect("/doctors")

# Route to manage the many-to-many relationship between patients and doctors
@app.route('/patients_per_doctor', methods=['POST', 'GET'])
def patients_per_doctor():
    if request.method == "GET":
        query = "SELECT * FROM Doctors_has_Patients;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        # Fetch doctor IDs
        doctors_query = "SELECT doctor_ID FROM Doctors;"
        doctors_cursor = db.execute_query(
            db_connection=db_connection, query=doctors_query)
        doctors_results = doctors_cursor.fetchall()

        # Fetch patient IDs
        patients_query = "SELECT patient_ID FROM Patients;"
        patients_cursor = db.execute_query(
            db_connection=db_connection, query=patients_query)
        patients_results = patients_cursor.fetchall()

        return render_template('patients_per_doctor.j2', patients_per_doctor=results, doctors=doctors_results, patients=patients_results)

    if request.method == "POST":
        if request.form.get("addPatientsPerDoctor"):
            doctor_ID = request.form['doctor_ID']
            patient_ID = request.form['patient_ID']

            query = """
            INSERT INTO Doctors_has_Patients (doctor_ID, patient_ID)
            VALUES (%s, %s)
            """

            cur = mysql.connection.cursor()
            cur.execute(query, (doctor_ID, patient_ID))
            mysql.connection.commit()

            return redirect("/patients_per_doctor")

# Route to delete a relationship between a doctor and a patient by doctor and patient IDs
@app.route("/delete_patients_per_doctor/<int:doctor_ID>/<int:patient_ID>")
def delete_patients_per_doctor(doctor_ID, patient_ID):
    query = "DELETE FROM Doctors_has_Patients WHERE doctor_ID = %s AND patient_ID = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (doctor_ID, patient_ID))
    mysql.connection.commit()
    return redirect("/patients_per_doctor")

# Route to edit the relationship between doctors and patients
@app.route("/edit_patients_per_doctor", methods=["POST"])
def edit_patients_per_doctor():
    if request.method == "POST":
        doctor_ID = request.form['doctor_ID']
        patient_ID = request.form['patient_ID']

        # Update query to modify the patient associated with a specific doctor
        query = """
        UPDATE Doctors_has_Patients
        SET patient_ID = %s
        WHERE doctor_ID = %s
        """

        cur = mysql.connection.cursor()
        cur.execute(query, (patient_ID, doctor_ID))
        mysql.connection.commit()

        return redirect("/patients_per_doctor")

# Route to manage the many-to-many relationship between patients and diagnoses
@app.route('/diagnosis_per_patient', methods=['POST', 'GET'])
def diagnosis_per_patient():
    if request.method == "GET":
        query = "SELECT * FROM Patients_has_Diagnoses;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        # Fetch patient IDs
        patients_query = "SELECT patient_ID FROM Patients;"
        patients_cursor = db.execute_query(
            db_connection=db_connection, query=patients_query)
        patients_results = patients_cursor.fetchall()

        # Fetch diagnosis IDs
        diagnosis_query = "SELECT diagnosis_ID FROM Diagnoses;"
        diagnosis_cursor = db.execute_query(
            db_connection=db_connection, query=diagnosis_query)
        diagnosis_results = diagnosis_cursor.fetchall()

        return render_template('diagnosisPerPatient.j2', diagnosis_per_patient=results, patients=patients_results, diagnosis=diagnosis_results)

    if request.method == "POST":
        if request.form.get("addDiagnosePerPatient"):
            patient_ID = request.form['patient_ID']
            diagnosis_ID = request.form['diagnosis_ID']

            print(f"Received data: {patient_ID}, {diagnosis_ID}")

            query = """
            INSERT INTO Patients_has_Diagnoses (patient_ID, diagnosis_ID)
            VALUES (%s, %s)
            """

            cur = mysql.connection.cursor()
            cur.execute(query, (patient_ID, diagnosis_ID))
            mysql.connection.commit()

            return redirect("/diagnosis_per_patient")

# Route to delete the relationship between a patient and a diagnosis by patient and diagnosis IDs
@app.route("/delete_diagnosis_per_patient/<int:patient_id>/<int:diagnosis_id>")
def delete_diagnosis_per_patient(patient_id, diagnosis_id):
    query = "DELETE FROM Patients_has_Diagnoses WHERE patient_ID = %s AND diagnosis_ID = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (patient_id, diagnosis_id))
    mysql.connection.commit()

    return redirect("/diagnosis_per_patient")

# Route to edit the relationship between a patient and a diagnosis
@app.route("/edit_diagnosis_per_patient", methods=["POST"])
def edit_diagnosis_per_patient():
    if request.method == "POST":
        patient_ID = request.form['patient_ID']
        diagnosis_ID = request.form['diagnosis_ID']

        # Update query to modify the diagnosis associated with a specific patient
        query = """
        UPDATE Patients_has_Diagnoses
        SET diagnosis_ID = %s
        WHERE patient_ID = %s
        """

        cur = mysql.connection.cursor()
        cur.execute(query, (diagnosis_ID, patient_ID))
        mysql.connection.commit()

        return redirect("/diagnosis_per_patient")

# Route to manage procedures, handles both GET (read) and POST (create)
@app.route('/procedures', methods=['POST', 'GET'])
def procedures():
    if request.method == "GET":
        query = "SELECT * FROM Procedures;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template('procedures.j2', procedures=results)

    if request.method == "POST":
        if request.form.get("addProcedure"):
            procedure_name = request.form['procedure_name']

            query = """
            INSERT INTO Procedures (procedure_name)
            VALUES (%s)
            """

            cur = mysql.connection.cursor()
            cur.execute(query, (procedure_name,))
            mysql.connection.commit()

            return redirect("/procedures")

# Route to delete a procedure by ID
@app.route("/delete_procedure/<int:id>")
def delete_procedure(id):
    query = "DELETE FROM Procedures WHERE procedure_ID = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/procedures")

# Route to edit procedure details
@app.route("/edit_procedure", methods=["POST"])
def edit_procedure():
    if request.method == "POST":
        procedure_ID = request.form['procedure_ID']
        procedure_name = request.form['procedure_name']

        # Update query to modify a procedure's details
        query = """
        UPDATE Procedures
        SET procedure_name = %s
        WHERE procedure_ID = %s
        """

        cur = mysql.connection.cursor()
        cur.execute(query, (procedure_name, procedure_ID))
        mysql.connection.commit()

        return redirect("/procedures")

# Route to manage diagnoses, handles both GET (read) and POST (create)
@app.route('/diagnoses', methods=['POST', 'GET'])
def diagnoses():
    if request.method == "GET":
        query = "SELECT * FROM Diagnoses;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        print(results)
        return render_template('diagnoses.j2', diagnoses=results)

    if request.method == "POST":
        if request.form.get("addDiagnosis"):
            diagnosis_ID = request.form['diagnosis_ID']
            disease_name = request.form['disease_name']

            print(f"Received data: {diagnosis_ID}, {disease_name}")

            query = """
            INSERT INTO Diagnoses (diagnosis_ID, disease_name)
            VALUES (%s, %s)
            """

            cur = mysql.connection.cursor()
            cur.execute(query, (diagnosis_ID, disease_name))
            mysql.connection.commit()

            return redirect("/diagnoses")

# Route to delete a diagnosis by ID
@app.route("/delete_diagnoses/<int:id>")
def delete_diagnoses(id):
    query = "DELETE FROM Diagnoses WHERE diagnosis_ID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/diagnoses")

# Route to edit diagnosis details
@app.route("/edit_diagnoses", methods=["POST"])
def edit_diagnoses():
    if request.method == "POST":
        diagnosis_ID = request.form['diagnosis_ID']
        disease_name = request.form['disease_name']

        # Update query to modify a diagnosis's details
        query = """
        UPDATE Diagnoses
        SET disease_name = %s
        WHERE diagnosis_ID = %s
        """

        cur = mysql.connection.cursor()
        cur.execute(query, (disease_name, diagnosis_ID))
        mysql.connection.commit()

        return redirect("/diagnoses")


if __name__ == "__main__":

    # Start the app on port 3000, it will be different once hosted
    app.run(port=50105, debug=True)
