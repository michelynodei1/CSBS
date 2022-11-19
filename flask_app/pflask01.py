# ///// IMPORTS /////
import os  # used to get environment variables IP & PORT
from flask import Flask  # Flask is the web app that we are customizing
from flask import render_template, request, redirect, url_for

# # ---Not Using Yet---
# from database import db  # importing database instance
# from models import Note as Note  # (Model names may change)
# from models import Note as Note  # (Model names may change)
# # -------------------

# ///// APP CREATION /////
app = Flask(__name__)

# ///// DATABASE CONFIG /////
# # --- Not Using Yet ---
# # Configure database connection
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'  # (db file name may change)
# # Disables a feature that signals the application every time a change is about to be made in the database
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Binds SQLAlchemy db object to this Flask app
# db.init_app(app)

# # Setup models
# with app.app_context():
    # db.create_all()  # Run under the app context
# # ---------------------


# ///// MOCK VARIABLES /////
# Project List
projects = {1: {'title': 'First Project'},
            2: {'title': 'Second Project'},
            3: {'title': 'Third Project'}
            }


# ///// ROUTES /////
# - Home | Overview -
@app.route('/')
def index():
    return render_template('index.html',)


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


# - My Work -
@app.route('/myWork')
def myWork():
    return render_template('myWork.html')


# - Task List -
@app.route('/taskList')
def taskList():
    return render_template('taskList.html')


# ///// HOST & PORT CONFIG /////
app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
