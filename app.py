from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)

@app.route("/", methods=['POST', 'GET'])
def index():
    task = Task.query.all()
    return render_template("home.html", task=task)

@app.route("/add", methods=['POST'])
def add():
    task_name = request.form.get('task_name')
    new_task = Task(task_name=task_name)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    db.create_all()#create the database
    app.run(debug=True)