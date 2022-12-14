# ///// IMPORTS /////
from __future__ import print_function
import os, sys, json, flask, flask_socketio, httplib2, uuid, bcrypt, sqlite3
from flask import Flask, Response, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from database import db
from models import User as User
from models import Note as Note
from models import Comment as Comment
from models import Project as Project
from models import Task as Task
from forms import RegisterForm, LoginForm, CommentForm
from flask_socketio import SocketIO, join_room


# ///// APP CREATION /////
app = Flask(__name__)  # create an app
socketio = SocketIO(app)


# ///// DATABASE CONFIG /////
# Configure database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
# Disables a feature that signals the application every time a change is about to be made in the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SE3155'

#  Binds SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all()  # Run under the app context


# ///// EVENTS /////
events = [
    {
        'title': 'Update Notes',
        'start': '2022-12-20',
        'end': '2022-12-20',
        'url': 'http://youtube.com',
    },
    {
        'title': 'Update List',
        'start': '2022-12-08',
        'end': '',
        'url': 'http://127.0.0.1:5000/taskList',
    },
]


# ///// ROUTES /////
# - Home -
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


# - Site Overview -
@app.route('/overview')
def overview():
    if session.get('user'):
        my_projects = db.session.query(Project).filter_by(user_id=session['user_id']).all()

        return render_template('overview.html', projects=my_projects, user=session['user'])
    else:
        return redirect(url_for('login'))


# - My Work -
@app.route('/myWork')
def myWork():
    return render_template('myWork.html')


@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html')


# ---------- Projects ----------
# - Projects List -
@app.route('/projects')
def projects_list():
    if session.get('user'):
        my_projects = db.session.query(Project).filter_by(user_id=session['user_id']).all()

        return render_template('projects_list.html', projects=my_projects, user=session['user'])
    else:
        return redirect(url_for('login'))


# - Add Project -
@app.route('/projects/create-project', methods=['GET', 'POST'])
def create_project():
    if session.get('user'):
        if request.method == 'POST':
            # get project title data
            title = request.form['title']
            # create date stamp
            from datetime import date
            today = date.today()
            # format date mm/dd/yyy
            today = today.strftime("%m-%d-%Y")

            new_record = Project(title, today, session['user_id'])
            db.session.add(new_record)
            db.session.commit()
            # ready to render response - redirect to projects list
            return redirect(url_for('projects_list'))
        else:
            # GET request - show 'create project' form
            return render_template('project_create.html', user=session['user'])
    else:
        return redirect(url_for('login'))


# - Specific Project Page -
@app.route('/projects/<project_id>')
def project_overview(project_id):
    if session.get('user'):
        p_id = project_id
        a_project = db.session.query(Project).filter_by(id=p_id).one()
        project_tasks = db.session.query(Task).filter_by(project_id=p_id).all()

        return render_template('project_overview.html', project=a_project, tasks=project_tasks, user=session['user'])
    else:
        return redirect(url_for('login'))


# - Edit Project -
@app.route('/projects/<project_id>/edit', methods=['GET', 'POST'])
def update_project(project_id):
    if session.get('user'):
        # check method used for request
        if request.method == 'POST':
            # get title data
            title = request.form['title']
            a_project = db.session.query(Project).filter_by(id=project_id).one()
            # update project data
            a_project.title = title
            # update project in DB
            db.session.add(a_project)
            db.session.commit()

            return redirect(url_for('projects_list'))
        else:
            # GET request - show create project form to edit project

            # retrieve project from database
            a_project = db.session.query(Project).filter_by(id=project_id).one()

            return render_template('project_create.html', project=a_project, user=session['user'])
    else:
        return redirect(url_for('login'))


# - Delete Project -
@app.route('/projects/<project_id>/delete', methods=['POST'])
def delete_project(project_id):
    if session.get('user'):
        # retrieve project from database
        a_project = db.session.query(Project).filter_by(id=project_id).one()
        db.session.delete(a_project)
        db.session.commit()

        return redirect(url_for('projects_list'))
    else:
        return redirect(url_for('login'))


# - Create Task for Project
@app.route('/projects/<project_id>/add-task', methods=['GET', 'POST'])
def add_task(project_id):
    if session.get('user'):
        if request.method == 'POST':
            # get task title data
            title = request.form['title']
            # get task description data
            desc = request.form['description']
            # create date stamp
            from datetime import date
            today = date.today()
            # format date mm/dd/yyy
            today = today.strftime("%m-%d-%Y")

            new_record = Task(title, desc, today, project_id)
            db.session.add(new_record)
            db.session.commit()
            # ready to render response - redirect to projects list
            return redirect(url_for('project_overview', project_id=project_id))
        else:
            # GET request - show 'add task' form
            return render_template('project_task_add.html', user=session['user'])
    else:
        return redirect(url_for('login'))


# - Edit Project Task -
@app.route('/projects/<project_id>/<task_id>/edit', methods=['GET', 'POST'])
def update_task(project_id, task_id):
    if session.get('user'):
        # check method used for request
        if request.method == 'POST':
            # get title data
            title = request.form['title']
            # get description data
            description = request.form['description']
            a_task = db.session.query(Task).filter_by(id=task_id).one()
            # update task data
            a_task.title = title
            # update task description
            a_task.description = description
            # update task in DB
            db.session.add(a_task)
            db.session.commit()

            return redirect(url_for('project_overview', project_id=project_id))
        else:
            # GET request - show create project form to edit project

            # retrieve task from database
            a_task = db.session.query(Task).filter_by(id=task_id).one()

            return render_template('project_task_add.html', task=a_task, user=session['user'])
    else:
        return redirect(url_for('login'))


# - Delete Project Task -
@app.route('/projects/<project_id>/<task_id>/delete', methods=['POST'])
def delete_task(project_id, task_id):
    if session.get('user'):
        # retrieve task from database
        a_task = db.session.query(Task).filter_by(id=task_id).one()
        db.session.delete(a_task)
        db.session.commit()

        return redirect(url_for('project_overview', project_id=project_id))
    else:
        return redirect(url_for('login'))


# -----------------------------------------------

# # - Progress Bar for Project Tasks -
# @app.route('/progress')
# def progress():
#     return render_template("progress.html")

# # - Completed Tasks -
# @app.route('/progress/done')
# def task_done(task_id):
#     if session.get('user'):
#         # retrieve task from database
#         total_tasks = db.session.query(Task).count()

#     return render_template("progress.html")


# # - Incomplete Tasks -
# @app.route('/progress/done')
# def task_done(task_id):
#     if session.get('user'):
#         # retrieve task from database
#         total_tasks = db.session.query(Task).count()

#     return render_template("progress.html")

# -----------------------------------------------


# ---------- Chat ----------
@app.route('/chat')
def chat():
    return render_template("chat.html")


# - Chatroom -
@app.route('/chatroom')
def chatroom():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template('chatroom.html', username=username, room=room)
    else:
        return redirect(url_for('chat'))


# - Send Message -
@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}:{}".format(data['username'], data['room'], data['message']))

    socketio.emit('receive_message', data, room=data['room'])


# - Join Room -
@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data)

# -----------------------------------------------


# ---------- To-Do List ----------
# - To-Do Overview -
@app.route('/taskList', methods=['GET', 'POST'])
def taskList():
    if request.method == 'POST':
        return redirect(url_for('myWork'))

    return render_template('taskList.html')


# ---------- Notes ----------
# - Notes Overview -
@app.route('/notes')
def get_notes():
    if session.get('user'):
        my_notes = db.session.query(Note).filter_by(user_id=session['user_id']).all()

        return render_template('notes.html', notes=my_notes, user=session['user'])
    else:
        return redirect(url_for('login'))


# - Specific Note Page -
@app.route('/notes/<note_id>')
def get_note(note_id):
    if session.get('user'):

        my_note = db.session.query(Note).filter_by(id=note_id, user_id=session['user_id']).one()
        form = CommentForm()

        return render_template('note.html', note=my_note, user=session['user'], form=form)
    else:
        return redirect(url_for('login'))


# - Add Note -
@app.route('/notes/new', methods=['GET', 'POST'])
def new_note():
    if session.get('user'):
        if request.method == 'POST':
            title = request.form['title']
            text = request.form['noteText']

            from datetime import date
            today = date.today()
            # format date mm/dd/yyyy
            today = today.strftime("%m-%d-%Y")

            new_record = Note(title, text, today, session['user_id'])
            db.session.add(new_record)
            db.session.commit()

            return redirect(url_for('get_notes'))
        else:
            a_user = db.session.query(User).filter_by(email='xdarkoh@uncc.edu').one()
            return render_template('new.html', user=session['user'])
    else:
        return redirect(url_for('login'))


# - Edit Note -
@app.route('/notes/edit/<note_id>', methods=['GET', 'POST'])
def update_note(note_id):
    # GET request - show new note form to edit note
    if session.get('user'):
        # Retrieve user from database

        if request.method == 'POST':
            title = request.form['title']

            text = request.form['noteText']

            note = db.session.query(Note).filter_by(id=note_id).one()

            note.title = title
            note.text = text

            db.session.add(note)
            db.session.commit()

            return redirect(url_for('get_notes'))
        else:

            my_note = db.session.query(Note).filter_by(id=note_id).one()
            # Removed user=session('user') in below render template
            return render_template('new.html', note=my_note, user=session['user'])
    else:
        return redirect(url_for('login'))


# - Delete Note -
@app.route('/notes/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    if session.get('user'):
        my_note = db.session.query(Note).filter_by(id=note_id).one()
        db.session.delete(my_note)
        db.session.commit()

        return redirect(url_for('get_notes'))
    else:
        return redirect(url_for('login'))


# - Add Comment -
# Fix functionality to work with the add task functions
@app.route('/notes/<note_id>/comment', methods=['POST'])
def new_comment(note_id):
    if session.get('user'):
        comment_form = CommentForm()
        # validate_on_submit only validates using POST
        if comment_form.validate_on_submit():
            # get comment data
            comment_text = request.form['comment']
            new_record = Comment(comment_text, int(note_id), session['user_id'])
            db.session.add(new_record)
            db.session.commit()

        return redirect(url_for('get_note', note_id=note_id))

    else:
        return redirect(url_for('login'))

# -----------------------------------------------


# ---------- User - Account ----------
# - User Registration -
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(first_name, last_name, request.form['email'], h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('login'))

    # something went wrong - display register view
    return render_template('register.html', form=form)


# - User Login -
@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('overview'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)


# - User Logout -
@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('home'))

# -----------------------------------------------


# ---------- Calendar ----------
# - Personal Calendar -
@app.route('/calendar')
def calendar():
    return render_template("calendar.html")


# - Group Calendar -
@app.route('/calendars')
def calendars():
    return render_template("calendars.html")

# -----------------------------------------------



# - Settings -
@app.route('/settings')
def settings():
    return render_template("settings.html")





# ///// HOST & PORT CONFIG /////
if __name__ == '__main__':
    # socketio.run(app, debug=True)
    socketio.run(app, host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
