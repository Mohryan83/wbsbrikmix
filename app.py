from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'rahasia123'  # Ganti dengan key rahasia asli

DATABASE = 'database/users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# ROUTE UTAMA
@app.route('/')
def index():
    return render_template('index.html')

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
            conn.commit()
            flash('Registrasi berhasil. Silakan login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email sudah terdaftar.', 'error')
        finally:
            conn.close()

    return render_template('register.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['email'] = user['email']
            return redirect(url_for('dashboard'))
        else:
            error = 'Email atau password salah.'

    return render_template('login.html', error=error)

# DASHBOARD SETELAH LOGIN
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return f"<h1>Selamat datang, {session['email']}!</h1><a href='/logout'>Logout</a>"
    return redirect(url_for('login'))

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    if not os.path.exists('database'):
        os.mkdir('database')
    app.run(debug=True)
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
@app.route('/syarat&ketentuan.html')
def syarat_ketentuan():
    return render_template('syarat&ketentuan.html')
