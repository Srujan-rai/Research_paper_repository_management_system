import mysql.connector
from flask import Flask, render_template, redirect, url_for, request
import hashlib

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
def home():
    return render_template("home.html", content="Welcome to Research Paper Repository")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user:
            if hashlib.sha256(password.encode()).hexdigest() == user[0]:
                return redirect(url_for('home'))
            else:
                return render_template('login.html', message='Invalid password')
        else:
            return render_template('login.html', message='Invalid username')

    return render_template("login.html")

@app.route('/create_user', methods=["POST"])
def create_user():
    if request.method == "POST":
        new_username = request.form["new_username"]
        new_password = request.form["new_password"]
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (new_username, hashed_password))
            connection.commit()
            return redirect(url_for('login'))  
        except mysql.connector.IntegrityError:
            return render_template('login.html', message='Username already exists')


if __name__ == "__main__":
    app.run(debug=True)
