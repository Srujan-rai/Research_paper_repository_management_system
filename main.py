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

    return render_template("index.html" , content=" Welcome to Research Paper Repository")






if __name__=="__main__":
    app.run(debug=True)