from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from decimal import Decimal
import MySQLdb.cursors
import re

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key'

# MySQL configuration
app.config['MYSQL_USER'] = 'philatelist_admin'
app.config['MYSQL_PASSWORD'] = 'your_password'  # Replace with the actual password for philatelist_admin
app.config['MYSQL_DB'] = 'philately_community'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form fields
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Input validation
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'error')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!', 'error')
        elif not username or not password or not email:
            flash('Please fill out the form!', 'error')
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            account = cursor.fetchone()
            if account:
                flash('Account already exists!', 'error')
            else:
                cursor.execute('INSERT INTO users (username, password, email) VALUES (%s, %s, %s)',
                               (username, password, email))
                mysql.connection.commit()
                flash('You have successfully registered!', 'success')
                return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('npda_dashboard'))
        else:
            flash('Incorrect username/password!', 'error')

    return render_template('login.html')

@app.route('/npda_dashboard', methods=['GET', 'POST'])
def npda_dashboard():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM npda WHERE user_id = %s', (session['id'],))
        account = cursor.fetchone()

        if request.method == 'POST':
            topup_amount = request.form['topup_amount']
            
            # Convert the top-up amount to Decimal
            new_balance = account['balance'] + Decimal(str(topup_amount))
            
            cursor.execute('UPDATE npda SET balance = %s WHERE user_id = %s', (new_balance, session['id']))
            mysql.connection.commit()
            flash('Balance topped up successfully!', 'success')
            return redirect(url_for('npda_dashboard'))

        return render_template('npda_dashboard.html', account=account)

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
