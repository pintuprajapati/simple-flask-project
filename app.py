from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# db configurations
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# To create the database (kind of migrations into the table)
with app.app_context():
    db.create_all()

# Model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String( 50), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == "GET":
        print('get')

    print('before post')
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(title=title, desc=desc) # creates a new instance of the Todo class
        db.session.add(todo) # adds the newly created Todo object to the current database session
        db.session.commit() # commits the changes made in the current database session to the actual database
        
        # now just refresh the page and this todo data will be added to db

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    print("➡ sno :", sno)
    todo = Todo.query.filter_by(sno=sno).first()
    print("➡ todo :", todo)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)