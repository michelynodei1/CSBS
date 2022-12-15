# ///// IMPORTS /////
import datetime
from database import db



# ///// MODELS /////
# - Users -
class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    notes = db.relationship("Note", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)
    projects = db.relationship("Project", backref="user", cascade="all, delete", lazy=True)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()


# - User / Notes -
class Note(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200))
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, title, text, date, user_id):
        self.title = title
        self.text = text
        self.date = date
        self.user_id = user_id


# - User / Comments -
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.VARCHAR, nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey("note.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # comments = db.relationship("Comment",backref ="note",cascade="all,delete-orphan",lazy=True) //ask tomorrow
    def __init__(self, content, note_id, user_id):
        self.date_posted = datetime.date.today()
        self.content = content
        self.note_id = note_id
        self.user_id = user_id


# - User / Projects -
class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column("title", db.String(200), nullable=False)
    created = db.Column("created", db.String(50), nullable=False)
    tasks = db.relationship("Task", backref="projects", cascade="all, delete", lazy=True)

    def __init__(self, title, created, user_id):
        self.title = title
        self.created = created
        self.user_id = user_id


# - User / Project / Tasks -
class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column("id", db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    title = db.Column("title", db.String(200), nullable=False)
    description = db.Column("description", db.String(200), nullable=False)
    created = db.Column("created", db.String(50), nullable=False)

    def __init__(self, title, desc, created, proj_id):
        self.title = title
        self.description = desc
        self.created = created
        self.project_id = proj_id
