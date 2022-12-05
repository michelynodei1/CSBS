# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template,request
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
from flask_socketio import SocketIO, join_room
app = Flask(__name__)     # create an app
socketio = SocketIO(app)

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

@app.route('/overview')
def overview():
    return render_template('overview.html')

@app.route('/myWork')
def myWork():
    return render_template('myWork.html')

#chat
@app.route('/chat')
def chat():
    return render_template("chat.html")

@app.route('/chatroom')
def chatroom():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template('chatroom.html',username=username,room=room)
    else:
        return redirect(url_for('chat'))
@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}:{}".format(data['username'],data['room'],data['message']))

    socketio.emit('receive_message', data, room=data['room'])

@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data)

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
        return redirect(url_for('get_notes'))

    # something went wrong - display register view
    return render_template('register.html', form=form)

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
            return redirect(url_for('get_notes'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)

@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('index'))

#Fix functionality to work with the add task functions 
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


if __name__ =='__main__':
    #socketio.run(app, debug=True)

    socketio.run(app,host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.