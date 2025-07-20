from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)

# Fungsi untuk membaca user dari file JSON
def load_users():
    with open('users.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user['email'] == email and user['password'] == password:
                return redirect(url_for('dashboard'))
        error = 'Email atau password salah!'
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    return '<h2>Selamat datang! Anda berhasil login.</h2>'

if __name__ == '__main__':
    app.run(debug=True)
