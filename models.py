from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
# This will be initialized in app.py

db = SQLAlchemy()


class User(db.Model):
    """Represents a registered user."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    google_id = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)

    tasks = db.relationship('Task', backref='user', lazy=True)


class Task(db.Model):
    """Represents a task belonging to a user."""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    deadline = db.Column(db.Date, nullable=True)
    quadrant = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
