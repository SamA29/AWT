
#Python Kanban Web Application

from flask import Flask, render_template,request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import mysql.connector

app = Flask(__name__)

#Custom secret key
app.secret_key = 'asdfghjkl'

#Database Connectionssss
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'NissanGTR!'
app.config['MYSQL_DB'] = 'kanban'


mysql = MySQL(app)


#Login code taken from codeshack.io
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #create variables
        username = request.form['username']
        password = request.form['password']
        #check account exists
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        #Fetch the record
        account = cursor.fetchone()
        
        if account:
        #create session here
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
        #redirect to homepage
        return 'Logged in successfully!'
    else:
        msg = 'Incorrect username or password. They are case sensitive!'
        
        #LOGIN FORM HERE
    return render_template('login.html', msg=msg)

@app.route('/login/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    return redirect(url_for('login'))

@app.route('/login/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        #create account here
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        #check account exists yet
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', [username])
        account = cursor.fetchone()
        #Validation checks for the registration
        if account:
            msg= 'Account with those credentials already exists'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid e-mail. Please check your email and try again'
        elif not username or not password or not email:
            msg = 'please fill out the form'
    elif request.method == 'POST':
        msg = 'please register by filling out the form'

    return render_template('register.html', msg=msg)

@app.route('/Kanban/')
def Select():
    return 'Login success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)