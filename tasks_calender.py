from flask import Flask, render_template, request, redirect, url_for
import json, os
from datetime import datetime

app = Flask(__name__)
TASK_FILE = 'tasks_calender.json'

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASK_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)  

def calendar(tasks, selected_date):
    grouped_tasks = {}
    for i, task in enumerate(tasks):
        task = task.copy()
        task['index'] = i
        if selected_date and task['date'] != selected_date:
            continue
        grouped_tasks.setdefault(task['date'], []).append(task)
    return grouped_tasks

@app.route('/calender/')
def index():
    tasks = load_tasks()
    # print('Tasks are : ', tasks)
    # print('Request is : ', request)
    selected_date = request.args.get('date')
    grouped_tasks = calendar(tasks, selected_date)
    return render_template('tasks_calender.html', grouped_tasks=grouped_tasks, selected_date=selected_date)

@app.route('/add/', methods=['POST'])
def add():
    text = request.form['task']
    if text:
        tasks = load_tasks()
        task_data = {'task': text, 'done': False, 'date': datetime.now().strftime('%Y-%m-%d')}
        tasks.append(task_data)
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]['done'] = not tasks[task_id]['done']
        save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
