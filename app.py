from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
TODO_FILE = 'toko.json'

#タスクの読み込み
def load_tasks():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    return []

#タスクの保存
def save_tasks(tasks):
    with open(TODO_FILE,"w",encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    if task:
        tasks = load_tasks()
        tasks.append({"task": task, "done": False})
        save_tasks(tasks)
    return redirect("/")

@app.route("/done/<int:task_id>")
def done(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = not tasks[task_id]["done"]
        save_tasks(tasks)
    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)