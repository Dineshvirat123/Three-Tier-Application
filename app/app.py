from flask import Flask, render_template, request, redirect, session
from db import get_db
import bcrypt

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

    # ✅ FIXED PASSWORD CHECK
    if user and bcrypt.checkpw(password.encode(), user[3]):
        session['user'] = user[1]
        return redirect('/dashboard')

    return "Invalid credentials"


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ---------- DASHBOARD ----------

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')

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


# ---------- PROJECTS ----------

@app.route('/projects', methods=['GET','POST'])
def projects():
    if 'user' not in session:
        return redirect('/')

    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']

        cur.execute("INSERT INTO projects (title, description) VALUES (%s, %s)", (title, desc))
        db.commit()

    cur.execute("SELECT * FROM projects")
    data = cur.fetchall()

    return render_template('projects.html', projects=data)


# ---------- BLOGS ----------

@app.route('/blogs', methods=['GET','POST'])
def blogs():
    if 'user' not in session:
        return redirect('/')

    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        cur.execute("INSERT INTO blogs (title, content) VALUES (%s, %s)", (title, content))
        db.commit()

    cur.execute("SELECT * FROM blogs")
    data = cur.fetchall()

    return render_template('blogs.html', blogs=data)


# ---------- IDEAS ----------

@app.route('/ideas', methods=['GET','POST'])
def ideas():
    if 'user' not in session:
        return redirect('/')

    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        idea = request.form['idea']

        cur.execute("INSERT INTO ideas (idea) VALUES (%s)", (idea,))
        db.commit()

    cur.execute("SELECT * FROM ideas")
    data = cur.fetchall()

    return render_template('ideas.html', ideas=data)


# ---------- RUN ----------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
