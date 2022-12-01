# ///// IMPORTS /////
import os  # used to get environment variables IP & PORT
from flask import Flask  # Flask is the web app that we are customizing
from flask import render_template, request, redirect, url_for

# # ---Not Using Yet---
# from database import db  # importing database instance
# from models import Note as Note  # (Model names may change -Rachel)
# from models import Note as Note  # (Model names may change -Rachel)
# from flask import session
# import bcrypt
# from models import Comment as Comment
# from forms import RegisterForm, LoginForm, CommentForm
# # -------------------


# ///// APP CREATION /////
app = Flask(__name__)

# ///// DATABASE CONFIG /////
# # --- Not Using Yet ---
# # Configure database connection
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'  # (db file name may change -Rachel)
# # Disables a feature that signals the application every time a change is about to be made in the database
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'SE3155'

# # Binds SQLAlchemy db object to this Flask app
# db.init_app(app)

# # Setup models
# with app.app_context():
# db.create_all()  # Run under the app context
# # ---------------------


# ///// MOCK VARIABLES /////
# User Info
user_info = {'name': 'Team CSBS'}

# Project List
projects = {1: {'title': 'First Project'},
            2: {'title': 'Second Project'},
            3: {'title': 'Third Project'}
            }

# Task List
tasks = {1: {'title': 'First Task', 'text': 'This is the first task'},
         2: {'title': 'Second Task', 'text': 'This is the second task'},
         3: {'title': 'Third Task', 'text': 'This is the third task'}
         }


# ///// ROUTES /////
# - Home | Overview -
@app.route('/')
def index():
    return render_template('index.html', )


# - Projects List -
@app.route('/projects')
def projects_list():
    return render_template('projects_list.html', projects=projects)


# - Add Project -
@app.route('/projects/create-project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        # get project title data
        title = request.form['title']
        # get the last ID used and increment by 1
        p_id = len(projects) + 1
        # create new project
        projects[p_id] = {'title': title}
        # ready to render response - redirect to projects list
        return redirect(url_for('projects_list'))
    else:
        # GET request - show 'create project' form
        return render_template('create_project.html')


# - Specific Project Page -
@app.route('/projects/<project_id>')
def project_overview(project_id):
    return render_template('project_overview.html', project=projects[int(project_id)])


# - My Work -
@app.route('/myWork')
def my_work():
    return render_template('myWork.html')


# - Task List -
@app.route('/task-list', methods=['GET', 'POST'])
def task_list():
    if request.method == 'POST':
        return redirect(url_for('Overview'))

    return render_template('taskList.html')


# !!! BELOW IS ALL WORK-IN-PROGRESS !!!
# # Brought in from Flask#06
# @app.route('/notes')
# def get_notes():
#     if session.get('user'):
#         my_notes = db.session.query(Note).filter_by(user_id=session['user_id']).all()
#
#         return render_template('notes.html', notes=my_notes, user=session['user'])
#     else:
#         return redirect(url_for('login'))
#
#
# # Brought in from Flask#06
# @app.route('/notes/<note_id>')
# def get_note(note_id):
#     if session.get('user'):
#
#         my_note = db.session.query(Note).filter_by(id=note_id)
#
#         form = CommentForm()
#
#         return render_template('note.html', note=my_note, user=session['user'], form=form)
#     else:
#         return redirect(url_for('login'))
#
#
# # Brought in from Flask#06
# @app.route('/notes/new', methods=['GET', 'POST'])
# def new_note():
#     if session.get('user'):
#         if request.method == 'POST':
#             title = request.form['title']
#             text = request.form['noteText']
#
#             from datetime import date
#             today = date.today()
#             # format date mm/dd/yyyy
#             today = today.strftime("%m-%d-%Y")
#
#             new_record = Note(title, text, today, session['user_id'])
#             db.session.add(new_record)
#             db.session.commit()
#
#             return redirect(url_for('get_notes'))
#         else:
#             a_user = db.session.query(User).filter_by(email='xdarkoh@uncc.edu').one()
#             return render_template('new.html', user=session['user'])
#     else:
#         return redirect(url_for('login'))
#
#
# @app.route('/notes/edit/<note_id>', methods=['GET', 'POST'])
# def update_note(note_id):
#     # GET request - show new note form to edit note
#     if session.get('user'):
#         # Retrieve user from database
#
#         if request.method == 'POST':
#             title = request.form['title']
#
#             text = request.form['noteText']
#
#             note = db.session.query(Note).filter_by(id=note_id).one()
#
#             note.title = title
#             note.text = text
#
#             db.session.add(note)
#             db.session.commit()
#
#             return redirect(url_for('get_notes'))
#         else:
#
#             my_note = db.session.query(Note).filter_by(id=note_id).one()
#             # Removed user=session('user') in below render template
#             return render_template('new.html', note=my_note)
#     else:
#         return redirect(url_for('login'))
#
#
# @app.route('/notes/delete/<note_id>', methods=['POST'])
# def delete_note(note_id):
#     if session.get('user'):
#         my_note = db.session.query(Note).filter_by(id=note_id).one()
#         db.session.delete(my_note)
#         db.session.commit()
#
#         return redirect(url_for('get_notes'))
#     else:
#         return redirect(url_for('login'))
#
#
# @app.route('/register', methods=['POST', 'GET'])
# def register():
#     form = RegisterForm()
#
#     if request.method == 'POST' and form.validate_on_submit():
#         # salt and hash password
#         h_password = bcrypt.hashpw(
#             request.form['password'].encode('utf-8'), bcrypt.gensalt())
#         # get entered user data
#         first_name = request.form['firstname']
#         last_name = request.form['lastname']
#         # create user model
#         new_user = User(first_name, last_name, request.form['email'], h_password)
#         # add user to database and commit
#         db.session.add(new_user)
#         db.session.commit()
#         # save the user's name to the session
#         session['user'] = first_name
#         session['user_id'] = new_user.id  # access id value from user model of this newly added user
#         # show user dashboard view
#         return redirect(url_for('get_notes'))
#
#     # something went wrong - display register view
#     return render_template('register.html', form=form)
#
#
# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     login_form = LoginForm()
#     # validate_on_submit only validates using POST
#     if login_form.validate_on_submit():
#         # we know user exists. We can use one()
#         the_user = db.session.query(User).filter_by(email=request.form['email']).one()
#         # user exists check password entered matches stored password
#         if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
#             # password match add user info to session
#             session['user'] = the_user.first_name
#             session['user_id'] = the_user.id
#             # render view
#             return redirect(url_for('get_notes'))
#
#         # password check failed
#         # set error message to alert user
#         login_form.password.errors = ["Incorrect username or password."]
#         return render_template("login.html", form=login_form)
#     else:
#         # form did not validate or GET request
#         return render_template("login.html", form=login_form)
#
#
# @app.route('/logout')
# def logout():
#     # check if a user is saved in session
#     if session.get('user'):
#         session.clear()
#
#     return redirect(url_for('index'))
#
#
# @app.route('/notes/<note_id>/comment', methods=['POST'])
# def new_comment(note_id):
#     if session.get('user'):
#         comment_form = CommentForm()
#         # validate_on_submit only validates using POST
#         if comment_form.validate_on_submit():
#             # get comment data
#             comment_text = request.form['comment']
#             new_record = Comment(comment_text, int(note_id), session['user_id'])
#             db.session.add(new_record)
#             db.session.commit()
#
#         return redirect(url_for('get_note', note_id=note_id))
#
#     else:
#         return redirect(url_for('login'))

# ///// HOST & PORT CONFIG /////
app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
