from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect("todo_list.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT CHECK(status IN ('Pending', 'Completed')) NOT NULL DEFAULT 'Pending'
        )
    """)
    conn.commit()
    conn.close()

create_table()

@app.route("/")
def index():
    conn = sqlite3.connect("todo_list.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    conn = sqlite3.connect("todo_list.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/update/<int:task_id>", methods=["POST"])
def update(task_id):
    new_title = request.form["new_title"]
    conn = sqlite3.connect("todo_list.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title=? WHERE id=?", (new_title, task_id))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/complete/<int:task_id>")
def complete(task_id):
    conn = sqlite3.connect("todo_list.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status='Completed' WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete(task_id):
    conn = sqlite3.connect("todo_list.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
