from datetime import datetime
import os
from functools import wraps


from dotenv import load_dotenv



from flask import Flask, render_template, request, redirect, url_for, session



from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    abort,
)


from authlib.integrations.flask_client import OAuth


from models import db, User, Task

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///schedulist.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = os.environ["SECRET_KEY"]

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




def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function




def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function



def get_user_task_or_404(task_id: int) -> Task:
    """Retrieve a task and ensure it belongs to the logged-in user."""
    task = Task.query.get_or_404(task_id)
    if task.user_id != session["user_id"]:
        abort(404)
    return task




@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    tasks_by_quadrant = {

        q: Task.query.filter_by(user_id=user_id, quadrant=q).all() for q in range(1, 5)

        q: (
            Task.query.filter_by(user_id=user_id, quadrant=q)
            .order_by(Task.deadline)
            .all()
        )
        for q in range(1, 5)

    }
    return render_template(
        "index.html", tasks=tasks_by_quadrant, user=session.get("user")
    )



@app.route("/tasks/<int:task_id>/toggle")
@login_required
def toggle_task(task_id: int):

    task = Task.query.filter_by(id=task_id, user_id=session["user_id"]).first_or_404()


    task = get_user_task_or_404(task_id)


@app.route("/tasks/<int:task_id>/toggle")
@login_required
def toggle_task(task_id: int):
    task = Task.query.filter_by(id=task_id, user_id=session["user_id"]).first_or_404()

    
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

    user = User.query.filter_by(google_id=user_info["sub"]).first()
    if user is None:
        email = user_info.get("email")
        if email is None:
            abort(400, description="Email claim missing from user info")
        user = User(
            username=email,
            google_id=user_info["sub"],

            email=user_info.get("email"),

            email=email,

        )
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


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_task():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form.get("description")
        deadline_str = request.form.get("deadline")
        quadrant = int(request.form["quadrant"])
        task = Task(
            title=title,
            description=description,
            quadrant=quadrant,
            user_id=session["user_id"],
        )
        if deadline_str:
            task.deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add_task.html", user=session.get("user"))


@app.route("/task/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):

    task = Task.query.filter_by(id=task_id, user_id=session["user_id"]).first_or_404()


    task = Task.query.filter_by(id=task_id, user_id=session["user_id"]).first_or_404()

    task = get_user_task_or_404(task_id)


    if request.method == "POST":
        task.title = request.form["title"]
        task.description = request.form.get("description")
        deadline_str = request.form.get("deadline")
        task.deadline = (
            datetime.strptime(deadline_str, "%Y-%m-%d").date() if deadline_str else None
        )
        task.quadrant = int(request.form["quadrant"])
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit_task.html", task=task, user=session.get("user"))


@app.route("/task/<int:task_id>/delete", methods=["GET", "POST"])
@login_required
def delete_task(task_id):

    task = Task.query.filter_by(id=task_id, user_id=session["user_id"]).first_or_404()


    task = Task.query.filter_by(id=task_id, user_id=session["user_id"]).first_or_404()

    task = get_user_task_or_404(task_id)


    if request.method == "POST":
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("delete_task.html", task=task, user=session.get("user"))





if __name__ == "__main__":


    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    app.run()

