from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

# In-memory list of todos: [id, title, status]
todos = []

@app.route('/')
def index():
    return render_template('index.html', tasks=todos)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        task_id = len(todos) + 1
        todos.append([task_id, title, 'Pending'])
    return redirect('/')

@app.route('/complete/<int:task_id>')
def complete(task_id):
    for task in todos:
        if task[0] == task_id:
            task[2] = 'Completed'
            break
    return redirect('/')

@app.route('/update/<int:task_id>', methods=['POST'])
def update(task_id):
    new_title = request.form.get('new_title')
    for task in todos:
        if task[0] == task_id:
            task[1] = new_title
            break
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete(task_id):
    global todos
    todos = [task for task in todos if task[0] != task_id]
    return redirect('/')

# Deployment support for Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
