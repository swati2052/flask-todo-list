from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Todo Model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

# Home Route - View & Add Todos
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('home'))

    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

# Update Todo Route
@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == "POST":
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("update.html", todo=todo)

# Delete Todo Route
@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('home'))

# Optional Debug Route - Show all todos
@app.route("/show")
def show():
    allTodo = Todo.query.all()
    return "<br>".join([f"{t.sno}: {t.title} - {t.desc}" for t in allTodo])

# Optional: Products Page
@app.route("/products")
def products():
    return "This is the product page"

# Main Entry
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
