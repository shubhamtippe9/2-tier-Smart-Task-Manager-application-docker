from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime
import time

app = Flask(__name__)

# Wait for DB to be ready
time.sleep(10)

db = mysql.connector.connect(
    host="db",
    user="root",
    password="root",
    database="tasksdb"
)

cursor = db.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    status VARCHAR(50),
    created_at TIMESTAMP
)
""")

@app.route('/')
def index():
    cursor.execute("SELECT * FROM tasks")
    data = cursor.fetchall()
    return render_template('index.html', tasks=data)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    cursor.execute(
        "INSERT INTO tasks (title, status, created_at) VALUES (%s, %s, %s)",
        (title, "Pending", datetime.now())
    )
    db.commit()
    return redirect('/')

@app.route('/complete/<int:id>')
def complete(id):
    cursor.execute("UPDATE tasks SET status='Completed' WHERE id=%s", (id,))
    db.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM tasks WHERE id=%s", (id,))
    db.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)