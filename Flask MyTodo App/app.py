from flask import Flask , render_template , request , redirect , flash  ## Importing
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# initialization 
app = Flask(__name__)  ## Initializing
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'   ## Original String 'sqlite:////tmp/test.db'
app.secret_key = "Todo_APP"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

### TO GET A LIST OF TABLES IN DB REFER -https://docs.sqlalchemy.org/en/14/core/reflection.html#fine-grained-reflection-with-inspector

class Todo(db.Model):
    sno = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(200) , nullable = False)
    description = db.Column(db.String(500) , nullable = False)
    date_created = db.Column(db.DateTime , default = datetime.utcnow)

    def __repr__(self):
        return '{} - {}'.format(self.sno,self.title)

class ContactUs(db.Model):
    query_no = db.Column(db.Integer , primary_key=True)
    email =  db.Column(db.String(100) , nullable=False)
    query_description = db.Column(db.String(1000) , nullable=False)

    def __repr__(self):
        return '{} - {}'.format(self.email,self.query_description)
 
@app.route('/automatic_todo')  ## Endpoints 
def automatic_todo():
    todo = Todo(title="First Todo", description ="Write all your Todo's" )
    db.session.add(todo)
    db.session.commit()
    return "<h1> Your First Todo Added </h1>"

@app.route('/', methods=['GET','POST'])
def home():
    
    if request.method =='POST':
        title = request.form["title"]
        desc = request.form["desc"]
        todo = Todo(title = title , description = desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html',allTodo=allTodo)


@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.description = desc
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
    

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/about_us')
def about_us():
    return render_template('/aboutus.html')

@app.route('/contact_us',methods=['GET','POST'])
def contact_us():
    if request.method == 'POST':
        flash('We will get back to you ASAP!!')
        email = request.form['email']
        query = request.form['query']
        contactus = ContactUs(email=email,query_description=query)
        print(contactus)
        db.session.add(contactus)
        db.session.commit()
        return render_template('contactus.html')
        
        # print(email+ '-' +query_description)
    return render_template('contactus.html')

## NOTE: Query was overiting the sqlite inbuilt query ref - https://stackoverflow.com/questions/16589208/attributeerror-while-querying-neither-instrumentedattribute-object-nor-compa#:~:text=I%20was%20getting,TEXT%2C%20name%3D%27query_text%27).

@app.route('/all_queries')
def all_queries():
    allQueries = ContactUs.query.all()
    return render_template('display_queries.html',allQueries=allQueries)

if __name__ == '__main__':  ## Running the app
    app.run(debug=True)