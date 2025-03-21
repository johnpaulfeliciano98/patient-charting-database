# Patient Charting Database Project

## Overview

The Patient Charting Database Project is a web-based application developed for Evergreen Health Clinic. This project streamlines patient information management, clinic operations, and medical records using a robust Flask-based web interface and a well-normalized MariaDB/MySQL database.

## Features

- **Patient Management:**  
  Perform full CRUD operations for patient records (personal details, diagnoses, procedures).

- **Clinic & Doctor Management:**  
  Manage clinics and doctors, including handling many-to-many relationships (Patients–Doctors).

- **Diagnosis & Procedures:**  
  Record and manage diagnoses and procedures with integrated validation and error handling.

- **User-Friendly Interface:**  
  Custom form validations, dropdown menus, and UI enhancements for an improved user experience.

- **Database Normalization:**  
  Efficient schema design using primary and foreign keys to ensure data integrity and minimize redundancy.

## Technologies Used

- **Backend:** Flask (Python)
- **Database:** MariaDB/MySQL
- **Frontend:** HTML, CSS, JavaScript

## Database Setup

The project includes an SQL dump file (`sql_file.sql`) that sets up the necessary tables, indexes, and constraints. To set up the database:

1. Ensure you have MariaDB/MySQL installed.
2. Run the SQL dump file using your preferred tool (e.g., phpMyAdmin) or via the command line:
   
       mysql -u your_username -p your_database < sql_file.sql

### SQL Schema Overview

The SQL file creates and populates the following tables:
- **Clinics**
- **Diagnoses**
- **Doctors**
- **Doctors_has_Patients**
- **Patients**
- **Patients_has_Diagnoses**
- **Procedures**

For full details, review the contents of the SQL file provided.

## Application Setup

1. **Clone the Repository:**
   
       git clone https://github.com/<your-username>/patient-charting-database.git
       cd patient-charting-database

2. **Configure the Application:**

   Update the `app.py` file with your MySQL database credentials:
   - `MYSQL_HOST`
   - `MYSQL_USER`
   - `MYSQL_PASSWORD`
   - `MYSQL_DB`

3. **Install Dependencies:**
   
       pip install -r requirements.txt

4. **Run the Application:**
   
       python app.py

   The application will run on port 50105 by default. Open your browser and navigate to [http://localhost:50105](http://localhost:50105).

## Code Structure

### SQL File
The `sql_file.sql` contains commands to:
- Drop existing tables.
- Create and populate the tables for Clinics, Diagnoses, Doctors, Patients, Procedures, and their relationship tables.
- Define indexes and constraints (including primary keys, foreign keys, and auto-increment settings).

### Application (app.py)
The `app.py` file is the main Flask application. It defines routes to:
- View, add, edit, and delete records for clinics, patients, doctors, diagnoses, and procedures.
- Manage many-to-many relationships (e.g., Doctors_has_Patients and Patients_has_Diagnoses).

Below is an abbreviated excerpt from `app.py` to illustrate the structure:

~~~python
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from database import db_connector as db

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = ''           # Enter your username
app.config['MYSQL_PASSWORD'] = ''       # Enter your password (last 4 of ONID)
app.config['MYSQL_DB'] = ''             # Enter your database name
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

# Establish database connection
db_connection = db.connect_to_database()
mysql = MySQL(app)

@app.route('/clinics')
def clinics():
    query = "SELECT * FROM Clinics;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('clinics.j2', clinics=results)

# Additional routes for patients, doctors, diagnoses, procedures, and relationships...

if __name__ == "__main__":
    app.run(port=50105, debug=True)
