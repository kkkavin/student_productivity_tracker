from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# --- DATABASE HELPER ---
def get_db_connection():
    conn = sqlite3.connect('tracker.db')
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, subject TEXT, task TEXT, status TEXT)''')
    conn.commit()
    conn.close()

# Initialize DB immediately
init_db()

# --- ROUTES ---

# 1. The Home Page (View Tasks)
@app.route('/')
def index():
    conn = get_db_connection()
    # Get only pending tasks
    tasks = conn.execute('SELECT * FROM tasks WHERE status="Pending"').fetchall()
    conn.close()
    # Send the 'tasks' data to the HTML file
    return render_template('index.html', tasks=tasks)

# 2. Add a Task
@app.route('/add', methods=['POST'])
def add_task():
    subject = request.form['subject']
    task = request.form['task']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (subject, task, status) VALUES (?, ?, ?)',
                 (subject, task, 'Pending'))
    conn.commit()
    conn.close()
    return redirect(url_for('index')) # Go back to home page

# 3. Mark Complete
@app.route('/complete/<int:id>')
def complete_task(id):
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET status="Completed" WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)