from flask import Flask, render_template, url_for, request, redirect
import logging
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time


app = Flask(__name__)

#Initialize Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = "Todo_List"
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        #Create a new Todo Object
        new_task = Todo(content = task_content)
        try:
            db.session.add(new_task)    #Add the Object to the database
            db.session.commit()         #Commit Changes made in session
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error while trying to add Task : {e}")
        return redirect('/')
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while deleting task : {e}")
    return redirect("/")

@app.route('/update/<int:id>', methods = ['POST','GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content'] #Does this automatically start a new session?

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error while Updating task : {e}")
        
        return redirect('/')


    else:
        return render_template('update.html', task = task)




if __name__ == "__main__":
    app.run(debug=True)
    

