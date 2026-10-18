
import os

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []
next_id = 1


@app.route("/")
def home():
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    global next_id

    title = request.form.get("title", "").strip()
    priority = request.form.get("priority", "Medium")

    if priority not in ["Low", "Medium", "High"]:
        priority = "Medium"

    if title:
        tasks.append({
            "id": next_id,
            "title": title,
            "priority": priority,
            "status": "To Do"
        })
        next_id += 1

    return redirect(url_for("home"))


@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            if task["status"] == "To Do":
                task["status"] = "In Progress"
            elif task["status"] == "In Progress":
                task["status"] = "Done"
            else:
                task["status"] = "To Do"
            break

    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    tasks[:] = [task for task in tasks if task["id"] != task_id]
    return redirect(url_for("home"))


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    # Local development only. In Docker the app is served by gunicorn.
    app.run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "1") == "1",
    )
