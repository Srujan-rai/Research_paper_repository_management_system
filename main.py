import mysql.connector
from flask import Flask,render_template,redirect,url_for,request
from mysql.connector import Error
app=Flask(__name__)
db={
        'host':'localhost',
        'database':'RESEARCH_PAPER_REPO',
        'user':'root',
        'password':'srujan123@RAI'
}
try:
    connection=mysql.connector.connect(**db)
    if connection.is_connected():
        print("database connected sucessfully")
    
except Error as e:
    print('error',e)
    
cursor=connection.cursor()

users = {
    'user1': 'password1',
    'user2': 'password2',
    'user3': 'password3'
}

@app.route('/')
def home():

    return render_template("home.html" , content=" Welcome to Research Paper Repository")


@app.route('/user',methods=['GET'])
def user():
    return "welcome user"

@app.route('/admin',methods=['GET'])
def admin():
    return "welcome admin"

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        if username in users and users[username]==password:
            return redirect(url_for("home"))
    else:
        return render_template("login.html")


if __name__=="__main__":
    app.run(debug=True)