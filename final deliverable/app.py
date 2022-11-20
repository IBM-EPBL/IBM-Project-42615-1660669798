from turtle import st
from flask import Flask, render_template, request, redirect ,url_for
import ibm_db


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32328;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=qgt90940;PWD=mDyHR77SnsqwVzAF",'','')

global login
login = False
app=Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index")
def index():
    return render_template("index.html")




@app.route('/addmember',methods = ['POST', 'GET'])
def addmember():
    if request.method == 'POST':
        name = request.form['first name']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        con_password = request.form['conform password']
        sql = "SELECT * FROM SIGNUP WHERE name =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,name)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            return render_template('signup.html', msg="You are already a member, please login using your details")
        else:
            insert_sql = "INSERT INTO SMART VALUES (?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, lastname)
            ibm_db.bind_param(prep_stmt, 3, email)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.bind_param(prep_stmt, 5, con_password)
            ibm_db.execute(prep_stmt)
        return render_template('signin.html', request="successfully created")


@app.route('/checkmember',methods = ['POST', 'GET'])
def check_member():
    global login
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM SMART WHERE email = '" + email +"'"
        stmt = ibm_db.exec_immediate(conn, sql)
        account = ibm_db.fetch_both(stmt)
        if not account:
            return render_template('login.html', msg = "enter valid email")
        if account['PASSWORD'] == password:
            login = True
            return redirect(url_for('main'))
        return render_template('login.html',msg2="invalid password")

@app.route('/signup',methods = ['POST', 'GET'])
def signup():
    global login
    login = False
    return render_template('singnin.html')

@app.route('/signin',methods = ['POST', 'GET'])
def signin():
    global login
    login = False
    return render_template('logoin.html')

@app.route('/main',methods = ['POST','GET'])
def main():
    return 'hello'