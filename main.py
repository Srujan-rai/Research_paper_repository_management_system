import mysql.connector
from flask import Flask, render_template, redirect, url_for, request,jsonify
import hashlib

department_id={
    "AIML":0,
    "CSE":1,
    "ISE":2,
    "EC":3,
    "MECH":4
}

app = Flask(__name__)
db = {
    'host': 'localhost',
    'database': 'RESEARCH_PAPER_REPO',
    'user': 'root',
    'password': 'srujan123@RAI'
}

try:
    connection = mysql.connector.connect(**db)
    if connection.is_connected():
        print("database connected successfully")
except mysql.connector.Error as e:
    print('error', e)

cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE,
                password VARCHAR(255))''')

@app.route('/') 
def login_redirect():
    return redirect(url_for("landing_page"))


    

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user:
            if hashlib.sha256(password.encode()).hexdigest() == user[0]:
                return render_template("home.html")
            else:
                return render_template('login.html', message='Invalid password')
        else:
            return render_template('login.html', message='Invalid username')

    return render_template("login.html")


@app.route('/create_user', methods=["POST"])
def create_user():
    if request.method == "POST":
        if 'new_username' in request.form and 'new_password' in request.form: 
            new_username = request.form["new_username"]
            new_password = request.form["new_password"]
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (new_username, hashed_password))
                connection.commit()
                return redirect(url_for('login'))  
            except mysql.connector.IntegrityError:
                return render_template('create_user.html', message='Username already exists')
        else:
            return render_template('create_user.html')
        
        
        
@app.route('/admin',methods=['GET','POST'])
def admin():
    
    return render_template("admin.html",content="welcome to the admin")

@app.route('/user',methods=['GET','POST'])
def user():
    if request.method == "POST":
        department = request.form['department']
        selected_options = request.form.getlist('selected_options[]')
        option_texts = {option: request.form.get(option) for option in selected_options}

        entered_values = {}
        for option in selected_options:
            entered_values[option] = {}
            for field in request.form:
                if field.startswith(option + '-'):
                    field_name = field.split('-', 1)[1]
                    entered_values[option][field_name] = request.form[field]

        print('Department:', department)
        print('Selected Options:', selected_options)
        print('Option Texts:', option_texts)
        print('Entered Values:', entered_values)

        
        
        
        

        if 'Consultancy' in selected_options:
            consultancy_data = entered_values['Consultancy']
            
            department_id_value = department_id.get(department, None)
            if department_id_value is not None:
                
                insert_statement = "INSERT INTO CONSULTANCY(DEPARTMENT_ID, AMOUNT_SANCTIONED, PRINCIPAL_INVESTIGATION, COPI, TITLE, AGENCY, YEAR,TYPE) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                
                data = (
                    department_id_value,
                    consultancy_data['Amount Sanctioned'],
                    consultancy_data['Principal investigation'],
                    consultancy_data['COPI'],
                    consultancy_data['Title'],
                    consultancy_data['Agency'],
                    consultancy_data['Year'],
                    consultancy_data['Type']
                )
                cursor.execute(insert_statement, data)
                connection.commit()
                print("data entered sucessfully!!! ")
                
            else:
                print("Department ID not found for department:", department)
        
        if 'ProductDevelopment' in selected_options:
            product_data = entered_values['ProductDevelopment']
            
            department_id_value = department_id.get(department, None)
            if department_id_value is not None:
                
                insert_statement = "INSERT INTO PRODUCTDEVELOPMENT(DEPARTMENT_ID, PRODUCT_TYPE, PRODUCT_DESCRIPTION, AREA_OF_APPLICATION, SPONSORING_FUNDING_AGENCY, FACULTY_MENTOR_NAME, STUDENT_NAME,STATUS) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                
                data = (
                    department_id_value,
                    product_data['Product Type'],
                    product_data['Product Description'],
                    product_data['Area of application'],
                    product_data['Sponsoring/Funding agency'],
                    product_data['Faculty Name/Mentor name'],
                    product_data['Student name'],
                    product_data['Status']
                )
                cursor.execute(insert_statement, data)
                connection.commit()
                print("data entered sucessfully!!! ")
                
            else:
                print("Department ID not found for department:", department)
        
        
        if 'Patent' in selected_options:
            patent_data = entered_values['Patent']
            
            department_id_value = department_id.get(department, None)
            if department_id_value is not None:
                
                insert_statement = "INSERT INTO PATENT (DEPARTMENT_ID, YEAR_OF_PUBLICATION, PRINCIPAL_INVESTIGATION, PATENT_NUMBER, TITLE, INDIAN_INTERNATIONAL, STATUS) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                
                data = (
                    department_id_value,
                    patent_data['Year of publication'],
                    patent_data['Principal investigation'],
                    patent_data['Patent number'],
                    patent_data['Title'],
                    patent_data['Indian/international'],
                    patent_data['Status']
                )
                cursor.execute(insert_statement, data)
                connection.commit()
                print("data entered sucessfully!!! ")
                
            else:
                print("Department ID not found for department:", department)
        
        
        if 'FDPWorkshopSeminarAttendedByFaculty' in selected_options:
            fdp_values=entered_values['FDPWorkshopSeminarAttendedByFaculty']
            department_id_value = department_id.get(department, None)
            if department_id_value is not None:
                insert_statement="INSERT INTO FDPWORKSHOPSEMINAR(DEPARTMENT_ID,DATE,TOPIC,DURATION,COORDINATION,ORGANIZER,FACULTY_NAME) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                data=(
                    department_id_value,
                    fdp_values['Date'],
                    fdp_values['Topic'],
                    fdp_values['Duration'],
                    fdp_values['Coordination'],
                    fdp_values['Organizer'],
                    fdp_values['Faculty Name']
    
                )
                try:
                   cursor.execute(insert_statement,data)
                   connection.commit()
                   print("data entered sucessfully")
                except mysql.connector.Error as e:
                 print('error', e)

            else:
                print("Department ID not found for department:", department) 
                
                
        if 'MOUCS' in selected_options:
            mou_values=entered_values['MOUCS']
            department_id_value = department_id.get(department, None)
            if department_id_value is not None:
                insert_statement="INSERT INTO MOUCS (DEPARTMENT_ID, DATE, MAJOR_AREA, TOPIC, DURATION, CERTIFIED_BY, ATTENDED_BY_FACULTY, ATTENDED_BY_STUDENT)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                data=(
                    department_id_value,
                    mou_values['Date'],
                    mou_values['Major area'],
                    mou_values['Topic'],
                    mou_values['Duration'],
                    mou_values['Certified by'],
                    mou_values['Faculty Name/USN'],
                    mou_values['Student Name/USN']
    
                )
                try:
                   cursor.execute(insert_statement,data)
                   connection.commit()
                   print("data entered sucessfully")
                except mysql.connector.Error as e:
                 print('error', e)

            else:
                print("Department ID not found for department:", department)
                
                
        if 'AchievementsAndAwards' in selected_options:
            award_values=entered_values['AchievementsAndAwards']
            department_id_value = department_id.get(department, None)
            if department_id_value is not None:
                insert_statement="INSERT INTO AchievementsAndAwards(DEPARTMENT_ID,DATE,EVENT_NAME,ORGANIZER,MENTOR_NAME,NAMES_OF_THE_FACULTY,TYPE_OF_PARTICIPATION,OUTCOMES) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                data=(
                    department_id_value,
                    award_values['Date'],
                    award_values['Event name'],
                    award_values['Organizer'],
                    award_values['Mentor name'],
                    award_values['Names of the faculty'],
                    award_values['Type of participation'],
                    award_values['Outcomes']
    
                )
                try:
                   cursor.execute(insert_statement,data)
                   connection.commit()
                   print("data entered sucessfully")
                except mysql.connector.Error as e:
                 print('error', e)

            else:
                print("Department ID not found for department:", department)    
                
        
        if 'MOUS' in selected_options:
            mous_values=entered_values['MOUS']
            department_id_value = department_id.get(department, None)
            if department_id_value is not None:
                insert_statement="INSERT INTO MOUS(DEPARTMENT_ID,DATE,DURATION,NAME_OF_THE_ORGANIZATION,TYPE_OF_MOU,OUTCOMES,FACULTY_INCHARGE) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                data=(
                    department_id_value,
                    mous_values['Date'],
                    mous_values['Duration'],
                    mous_values['Name of the organization'],
                    mous_values['Type of MOU'],
                    mous_values['Outcomes'],
                    mous_values['Faculty incharge']
                    )
                try:
                   cursor.execute(insert_statement,data)
                   connection.commit()
                   print("data entered sucessfully")
                except mysql.connector.Error as e:
                 print('error', e)

            else:
                print("Department ID not found for department:", department) 
          
        if 'FundedStudentProject' in selected_options:
            project_values=entered_values['FundedStudentProject']
            department_id_value = department_id.get(department, None)
            if department_id_value is not None:
                insert_statement="INSERT INTO FUNDEDSTUDENTPROJECT(DEPARTMENT_ID,YEAR_SANCTIONED,SUPERVISION,COSUPERVISION,STUDENT_NAME,TITLE_OF_THE_PROJECT ,FUNDING_AGENCIES,AMOUNT,STATUS) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                data=(
                    department_id_value,
                    project_values['Year sanctioned'],
                    project_values['Supervison'],
                    project_values['Cosupervision'],
                    project_values['Student Name'],
                    project_values['Title of the project'],
                    project_values['Funding Agencies'],
                    project_values['Amount'],
                    project_values['Status']
                    )
                try:
                   cursor.execute(insert_statement,data)
                   connection.commit()
                   print("data entered sucessfully")
                except mysql.connector.Error as e:
                 print('error', e)

            else:
                print("Department ID not found for department:", department) 
          
                   

        return render_template("user.html", message='hi hello')
    
    
        
    
    

    else:
        return render_template("user.html", message='Input not found')


@app.route('/landing_page',methods=['GET','POST'])
def landing_page():
    if request.method=="POST":
      return  redirect(url_for(login))
    else:
      return render_template("landing_page.html")




if __name__ == "__main__":
    app.run(debug=True)
