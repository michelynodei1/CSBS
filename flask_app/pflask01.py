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


# ///// ROUTES /////
# - Home | Overview -
@app.route('/')
def index():
    return render_template('index.html')


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
