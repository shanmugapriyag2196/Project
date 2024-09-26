from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Connect to the SQLite database (creates a new file if it doesn't exist)
def get_db_connection():
    conn = sqlite3.connect('user_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create a table to store usernames and passwords if it doesn't already exist
def create_table():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

create_table()

# Home route for login page
@app.route('/')
def home():
    return render_template('login.html')

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user:
        stored_password = user['password']
        # Check if the password matches the hashed password
        if bcrypt.checkpw(password, stored_password.encode('utf-8')):
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to dashboard
        else:
            flash('Invalid password', 'danger')
    else:
        flash('Username not found', 'danger')

    return redirect(url_for('home'))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']

        # Validation logic
        if not username or not password or not email:
            flash('Please fill out all fields', 'danger')
            return redirect(url_for('create_account'))

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('create_account'))

        # Check if the username already exists
        conn = get_db_connection()
        existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if existing_user:
            flash('Username already exists', 'danger')
            conn.close()
            return redirect(url_for('create_account'))

        try:
            # Hash the password before storing
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            print(f"Storing user: {username}, Email: {email}, Password (hashed): {hashed_password}")

            # Add the new user to the database
            conn.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', 
                         (username, hashed_password.decode('utf-8'), email))
            conn.commit()
            flash('Account created successfully!', 'success')
            print(f"User {username} inserted successfully!")

        except Exception as e:
            print(f"Error inserting user: {e}")
            flash('An error occurred while creating your account', 'danger')

        finally:
            conn.close()

        return redirect(url_for('home'))

    return render_template('create_account.html')


# Dashboard route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
