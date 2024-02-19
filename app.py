from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from datetime  import  datetime

task_app = Flask(__name__)
task_app.secret_key='my_key'

task_app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///task.db'

db = SQLAlchemy(task_app)

#creating table classes

class Users(db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    email= db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(100), nullable=False)
   
    

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = self._hash_password(password)

    def _hash_password(self, password):
        # Hash the password using bcrypt with automatically generated salt

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        return hashed_password.decode('utf-8')
    

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False,)
    status = db.Column(db.String(10), nullable=False, default=0)
    user_name = db.Column(db.String(200), nullable=False, unique=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'user_name': self.user_name,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }


#creating the Database with the tables
with task_app.app_context():
    db.create_all()
    print("done")

@task_app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response
#deining my apps routes 
@task_app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('landing.html')

@task_app.route('/login', methods=['GET', 'POST'])
def login():
    login_error = None
    if "name" in session:
        return redirect(url_for('mytasks'))
    
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = Users.query.filter_by(name=name).first()

        if user:
            # Use bcrypt to check if the provided password matches the stored hashed password
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                session["name"]=user.name
                #if the user has successfully
                    #get all the tasks created by user  
                all_tasks_objects = Tasks.query.filter_by(user_name=session["name"]).all()
                    #store each task information in a dictionary and all the tasks in a all_tasks_dictionnary
                all_tasks_dictionnary =  [task.to_dict() for task in all_tasks_objects]
                    #create a session and store all the dictionary inside it 
                session["tasks"]=all_tasks_dictionnary
                    #redirect user to tasks dashboard 
                return redirect(url_for('mytasks'))
            else:
                #if the name is correct but the password is wrong prints a login error
                login_error = "Incorrect UserName or Password"

        else:
            #if user_name does not  exist in the database tell the user to create an account
            login_error = "You are not registered yet please sign up"
    return render_template('index.html', login_error=login_error)

@task_app.route('/register',methods=['GET', 'POST'] )
def register():
    error_message = None
    #getting form information if there is post request if there is post request
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email'] 
        password = request.form['password']

        existing_user = Users.query.filter_by(name=name).first()


        if existing_user:
            error_message = 'Username already exists. Please choose a new a one.'
        else:
            new_user = Users(name=name, password=password, email=email)
            db.session().add(new_user)
            db.session().commit()
            return redirect('/logout')
    print("register")
    return render_template('register.html', error_message = error_message)





@task_app.route('/mytasks', methods=['GET', 'POST'])
def mytasks():
            
    if "name" in session:
        if request.method == 'POST':
            task_name = request.form['task_name'].capitalize()
            new_task = Tasks(name=task_name, user_name=session['name'])
            db.session().add(new_task)
            db.session().commit()
            print(session["tasks"])
            all_tasks_objects = Tasks.query.filter_by(user_name=session['name']).all()
            
            all_tasks_dictionnary =  [task.to_dict() for task in all_tasks_objects]
            session["tasks"]=all_tasks_dictionnary
        print(session["tasks"])
        return render_template('mytasks.html', user=session["name"], my_tasks=session["tasks"])
    else:
        return redirect(url_for("login"))

#endpoint for updtating tasks status 
@task_app.route('/update_status', methods=['GET', 'POST'])
def task_status():
    status = request.form.get('status')
    task_id = request.form.get('task_id')
    task = Tasks.query.get_or_404(int(task_id))
    if task:
        task.status = status
        db.session.commit()

        # Fetch the updated tasks and store them in the session
        all_tasks_objects = Tasks.query.filter_by(user_name=session["name"]).all()
        all_tasks_dictionnary =  [task.to_dict() for task in all_tasks_objects]
        session["tasks"] = all_tasks_dictionnary

    return redirect(url_for('login'))
    



   
@task_app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('name', None)
    return redirect(url_for("login")) 


@task_app.route('/delete/<int:id>')
def delete(id):
    #delete  a task based on its id 
    task_to_delete = Tasks.query.get(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    #updating the session 
    all_tasks_objects = Tasks.query.filter_by(user_name=session["name"]).all()
    all_tasks_dictionnary =  [task.to_dict() for task in all_tasks_objects]
    session["tasks"] = all_tasks_dictionnary


    return redirect(url_for("mytasks"))

@task_app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    print("###################")
    task_to_edit = Tasks.query.get(int(id))
    print(task_to_edit)
    if request.method == 'POST':
             print("###################")
             task_to_edit.name = request.form["taskNamee"]
    db.session.commit()

    #updating the session 
    all_tasks_objects = Tasks.query.filter_by(user_name=session["name"]).all()
    all_tasks_dictionnary =  [task.to_dict() for task in all_tasks_objects]
    session["tasks"] = all_tasks_dictionnary


    return redirect(url_for("mytasks")) 




if __name__ == "__main__":
    task_app.run(debug=True)