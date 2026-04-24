from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# 🔐 Change these passwords
SECRET_PASSWORD = "98409840"
ADMIN_PASSWORD = "ADMIN4304"

# 📦 Create database
def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  email TEXT UNIQUE)''')
    conn.commit()
    conn.close()

init_db()

# 🏠 Home page
@app.route('/')
def home():
    return render_template('form.html')

# ✅ Submit attendance
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    if password != SECRET_PASSWORD:
        return "❌ Wrong password!"

    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()

    try:
        c.execute("INSERT INTO attendance (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        message = "✅ Attendance marked!"
    except:
        message = "⚠️ Already submitted!"

    conn.close()
    return message

# 🔐 Admin login + view
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form['password'] != ADMIN_PASSWORD:
            return "❌ Wrong admin password!"

        conn = sqlite3.connect('attendance.db')
        c = conn.cursor()
        c.execute("SELECT * FROM attendance")
        data = c.fetchall()
        conn.close()

        return render_template('admin.html', data=data)

    return '''
        <h2>Admin Login</h2>
        <form method="post">
            Password: <input type="password" name="password">
            <button type="submit">Login</button>
        </form>
    '''

# ▶️ Run app
if __name__ == "__main__":
    app.run()
