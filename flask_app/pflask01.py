# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from models import User as User
from models import Note as Note
from flask import session
import bcrypt
from models import Comment as Comment
from database import db
from flask import session
from forms import RegisterForm, LoginForm, CommentForm

app = Flask(__name__)     # create an app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = 'SE3155'

#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all()   # run under the app context

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/myWork')
def myWork():
    return render_template('myWork.html')

#Brought in from Flask#06
@app.route('/notes')
def get_notes():

    if session.get('user'):
        my_notes = db.session.query(Note).filter_by(user_id=session['user_id']).all()

        return render_template('notes.html', notes=my_notes, user=session['user'])
    else:
        return redirect(url_for('login'))

#Brought in from Flask#06
@app.route('/notes/<note_id>')
def get_note(note_id):
 if session.get('user'):
     
     my_note = db.session.query(Note).filter_by(id=note_id)

     form = CommentForm()

     return render_template('note.html', note=my_note, user=session['user'], form=form)
 else:
     return redirect(url_for('login'))


#Brought in from Flask#06
@app.route('/notes/new', methods=['GET', 'POST'])
def new_note():

   if session.get('user'):
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['noteText']

        from datetime import date
        today = date.today()
        #format date mm/dd/yyyy
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

@app.route('/notes/edit/<note_id>', methods=['GET', 'POST'])
def update_note(note_id):
    #GET request - show new note form to edit note
  if session.get('user'):
    #Retrieve user from database

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
#Removed user=session('user') in below render template
        return render_template('new.html', note=my_note)
  else:
    return redirect(url_for('login'))


@app.route ('/notes/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    if session.get('user'):
        my_note= db.session.query(Note).filter_by(id=note_id).one()
        db.session.delete(my_note)
        db.session.commit()    

        return redirect(url_for('get_notes'))
    else:
        return redirect(url_for('login'))

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





@app.route('/taskList', methods=['GET', 'POST'])
def taskList():
    if request.method == 'POST':


        return redirect(url_for('index'))
        
    return render_template('taskList.html')



app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.