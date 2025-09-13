from datetime import datetime

import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

=======

=======



from models import db, User, Task


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedulist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get("SECRET_KEY", "dev")


oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
    client_kwargs={"scope": "openid email profile"},
)

db.init_app(app)

with app.app_context():
    db.create_all()
    # Create a default user for now until authentication is implemented
    if not User.query.first():
        demo = User(username="demo")
        db.session.add(demo)
        db.session.commit()


def login_required(f):
    """Decorator to require a logged-in user."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@login_required
def index():
    tasks_by_quadrant = {

        1: Task.query.filter_by(user_id=session["user_id"], quadrant=1).all(),
        2: Task.query.filter_by(user_id=session["user_id"], quadrant=2).all(),
        3: Task.query.filter_by(user_id=session["user_id"], quadrant=3).all(),
        4: Task.query.filter_by(user_id=session["user_id"], quadrant=4).all(),
=======
        1: Task.query.filter_by(quadrant=1).order_by(Task.deadline).all(),
        2: Task.query.filter_by(quadrant=2).order_by(Task.deadline).all(),
        3: Task.query.filter_by(quadrant=3).order_by(Task.deadline).all(),
        4: Task.query.filter_by(quadrant=4).order_by(Task.deadline).all(),

    }

    return render_template("index.html", tasks=tasks_by_quadrant, user=session.get("user"))


@app.route("/tasks/<int:task_id>/toggle")
def toggle_task(task_id: int):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/login")
def login():
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/login/callback")
def authorize():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    username = user_info.get("email")
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
    session["user_id"] = user.id
    session["user"] = user_info
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return redirect(url_for("index"))

=======

=======





@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description')
        deadline_str = request.form.get('deadline')
        quadrant = int(request.form['quadrant'])

        task = Task(title=title, description=description, quadrant=quadrant, user_id=session["user_id"])
        if deadline_str:
            task.deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()

        db.session.add(task)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_task.html')


@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form.get('description')
        deadline_str = request.form.get('deadline')
        task.deadline = (
            datetime.strptime(deadline_str, '%Y-%m-%d').date()
            if deadline_str
            else None
        )
        task.quadrant = int(request.form['quadrant'])
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task)


@app.route('/task/<int:task_id>/delete', methods=['GET', 'POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('delete_task.html', task=task)


if __name__ == '__main__':
    app.run()
