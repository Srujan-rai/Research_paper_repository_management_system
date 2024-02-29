import mysql.connector
from flask import Flask,render_template,redirect,url_for
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

@app.route('/')
def home():

    return render_template("home.html" , content=" Welcome to Research Paper Repository")


@app.route('/user',methods=['GET'])
def user():
    return "welcome user"

@app.route('/admin',methods=['GET'])
def admin():
    return "welcome admin"




if __name__=="__main__":
    app.run(debug=True)