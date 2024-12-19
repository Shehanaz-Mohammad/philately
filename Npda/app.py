import os
from flask_bcrypt import Bcrypt
import mysql.connector
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, request

app = Flask(__name__)
app.secret_key = 'your_secret_key'
all_stamps = [
    {'title': f'Stamp {i}', 'imageUrl': f'/static/images/stamp{i}.jpeg'} for i in range(1, 21)
]

@app.route('/load_stamps')
def load_stamps():
    page = int(request.args.get('page', 1))
    per_page = 6
    start = (page - 1) * per_page
    end = start + per_page
    stamps = all_stamps[start:end]
    return jsonify({'stamps': stamps})

bcrypt = Bcrypt(app)

# Configuration for file upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Khaja12300!",
        database="npda_db"
    )

# Allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('npda_profile', email=email))
        else:
            return "Invalid email or password", 401

    return render_template('login.html')

# Landing page route
@app.route('/')
def landing():
    return render_template('landing.html')

# Create NPDA account route
@app.route('/create_npda', methods=['GET', 'POST'])
def create_npda():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        aadhaar = request.form['aadhaar']
        balance = float(request.form['balance'])
        password = request.form['password']

        # Handling the document upload
        document = request.files['document']
        if document and allowed_file(document.filename):
            filename = secure_filename(document.filename)
            document.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return "Invalid file type!", 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (name, email, aadhaar, balance, document, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, email, aadhaar, balance, filename, hashed_password))
            conn.commit()
        except mysql.connector.Error as err:
            return f"Error: {err}", 500
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('login'))

    return render_template('create_npda.html')
@app.route('/mock-payment', methods=['POST'])
def mock_payment():
    # Simulate a successful payment
    return {
        'status': 'success',
        'message': 'Payment processed successfully!',
        'transaction_id': 'mock123456789'
    }, 200

# NPDA profile route
@app.route('/npda_profile')
def npda_profile():
    email = request.args.get('email')

    if not email:
        return "Email parameter is required!", 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            return "User not found!", 404

        # Fetch user's stamps
        cursor.execute("""
            SELECT s.* 
            FROM stamps st 
            JOIN stamp_store s ON st.stamp_id = s.id 
            WHERE st.user_id = %s
        """, (user['id'],))
        stamps = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('npda_profile.html', stamps=stamps, user=user)

    except Exception as e:
        return str(e), 500

# Buy stamps route
@app.route('/buy_stamps', methods=['POST'])
def buy_stamps():
    email = request.form['email']
    stamp_ids = request.form.getlist('stamp_ids')

    if not email or not stamp_ids:
        return "Email and stamp IDs are required!", 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            return "User not found!", 404

        user_id = user['id']
        for stamp_id in stamp_ids:
            cursor.execute("INSERT INTO stamps (user_id, stamp_id) VALUES (%s, %s)", (user_id, stamp_id))

        conn.commit()
        return "Stamps purchased successfully!", 200

    except Exception as e:
        return str(e), 500
    finally:
        cursor.close()
        conn.close()

# Route to handle gifting NPDA
@app.route('/gift_npda', methods=['GET', 'POST'])
def gift_npda():
    if request.method == 'POST':
        recipient_name = request.form['recipient_name']
        recipient_email = request.form['recipient_email']
        deposit_amount = float(request.form['deposit_amount'])
        postal_code = request.form['postal_code']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO gift_npda (recipient_name, recipient_email, deposit_amount, postal_code)
                VALUES (%s, %s, %s, %s)
            """, (recipient_name, recipient_email, deposit_amount, postal_code))
            conn.commit()
        except mysql.connector.Error as err:
            return f"Error: {err}", 500
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('login'))  # Redirect to the login page

    return render_template('gift_npda.html')

if __name__ == '__main__':
    app.run(debug=True)
