from flask import Flask, render_template, request, redirect, session
from db import get_db
import bcrypt
import os

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- AUTH ----------

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())

        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",
                    (name,email,password))
        db.commit()

        return redirect('/')
    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()

    if user and bcrypt.checkpw(password.encode(), user[3].encode()):
        session['user'] = user[1]
        return redirect('/dashboard')
    return "Invalid credentials"

# ---------- DASHBOARD ----------

@app.route('/dashboard')
def dashboard():
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT COUNT(*) FROM projects")
    projects = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM blogs")
    blogs = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM deployments")
    deployments = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM ideas")
    ideas = cur.fetchone()[0]

    return render_template(
        'dashboard.html',
        user=session.get('user'),
        projects=projects,
        blogs=blogs,
        deployments=deployments,
        ideas=ideas,
        version="v2.0",
        region="Mumbai",
        instance="i-123456"
    )

# ---------- SIMPLE ADD ----------

@app.route('/add_project', methods=['POST'])
def add_project():
    title = request.form['title']
    desc = request.form['description']

    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO projects (title,description) VALUES (%s,%s)", (title,desc))
    db.commit()

    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
