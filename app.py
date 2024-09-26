from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# In-memory users storage (for demonstration purposes)
users = {
    'testuser': {'username': 'Priya', 'password': '12345', 'email': 'shanmugapriyag@valueglobal.net'};
    'testuser1': {'username': 'Harshita', 'password': '12345', 'email': 'harshitar@valueglobal.net'};
    'testuser1': {'username': 'Shanmuga', 'password': 'Priya2196', 'email': 'gshanmugapriyaece@gmail.com'}
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Validate the username and password
    if username in users:
        if users[username]['password'] == password:
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
        if username in users:
            flash('Username already exists', 'danger')
            return redirect(url_for('create_account'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('create_account'))

        # Add the new user to the in-memory users dictionary
        users[username] = {'username': username, 'password': password, 'email': email}

        flash('Account created successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('create_account.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
