from datetime import datetime
import logging
import os
from functools import wraps

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
from dotenv import load_dotenv

from models import db, User, Task
from sqlalchemy import select

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///schedulist.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
try:
    app.secret_key = os.environ["SECRET_KEY"]
except KeyError as exc:
    raise RuntimeError("SECRET_KEY environment variable not set") from exc

oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

if not google.client_id:
    raise RuntimeError(
        "GOOGLE_CLIENT_ID is missing. Set the GOOGLE_CLIENT_ID environment variable or provide it in a .env file."
    )

if not google.client_secret:
    raise RuntimeError(
        "GOOGLE_CLIENT_SECRET is missing. Set the GOOGLE_CLIENT_SECRET environment variable or provide it in a .env file."
    )

db.init_app(app)


@app.errorhandler(403)
def forbidden(_):
    return render_template("403.html"), 403


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


def get_user_task_or_404(task_id: int, current_user: User) -> Task:
    """Retrieve a task and ensure it belongs to the logged-in user."""
    logger.info("User %s requesting task %s", current_user.id, task_id)
    task = db.session.get(Task, task_id)
    if task is None:
        abort(404)
    if task.user_id != current_user.id:
        logger.warning(
            "User %s forbidden from task %s owned by %s",
            current_user.id,
            task_id,
            task.user_id,
        )
        abort(403)
    return task


@app.route("/")
def root():
    return "Server is running"


@app.route("/dashboard")
@login_required
def index():
    user_id = session["user_id"]
    tasks_by_quadrant = {
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
    current_user = db.session.get(User, session["user_id"])
    if current_user is None:
        abort(404)
    task = get_user_task_or_404(task_id, current_user)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/login")
def login():
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/login/callback")
def authorize():
    try:
        google.authorize_access_token()
    except Exception as exc:  # pragma: no cover - oauth library error handling
        logger.exception("Failed to authorize access token: %s", exc)
        abort(400, description="Failed to authorize access token")

    try:
        resp = google.get("https://openidconnect.googleapis.com/v1/userinfo")
        user_info = resp.json()
    except Exception as exc:  # pragma: no cover - oauth library error handling
        logger.exception("Failed to fetch user info: %s", exc)
        abort(500, description="Failed to parse user information")

    user = db.session.execute(
        select(User).filter_by(google_id=user_info["sub"])
    ).scalar_one_or_none()
    if user is None:
        email = user_info.get("email")
        if email is None:
            abort(400, description="Email claim missing from user info")
        user = User(
            username=email,
            google_id=user_info["sub"],
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
            try:
                task.deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            except ValueError:
                error = "Invalid date format. Please use YYYY-MM-DD."
                return (
                    render_template(
                        "add_task.html", error=error, user=session.get("user")
                    ),
                    400,
                )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add_task.html", user=session.get("user"))


@app.route("/task/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    current_user = db.session.get(User, session["user_id"])
    if current_user is None:
        abort(404)
    task = get_user_task_or_404(task_id, current_user)

    if request.method == "POST":
        task.title = request.form["title"]
        task.description = request.form.get("description")
        deadline_str = request.form.get("deadline")
        if deadline_str:
            try:
                task.deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            except ValueError:
                error = "Invalid date format. Please use YYYY-MM-DD."
                return (
                    render_template(
                        "edit_task.html",
                        task=task,
                        error=error,
                        user=session.get("user"),
                    ),
                    400,
                )
        else:
            task.deadline = None
        task.quadrant = int(request.form["quadrant"])
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit_task.html", task=task, user=session.get("user"))


@app.route("/task/<int:task_id>/delete", methods=["GET", "POST"])
@login_required
def delete_task(task_id):
    current_user = db.session.get(User, session["user_id"])
    if current_user is None:
        abort(404)
    task = get_user_task_or_404(task_id, current_user)

    if request.method == "POST":
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("delete_task.html", task=task, user=session.get("user"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    debug = os.getenv("FLASK_DEBUG", "false").lower() in {
        "1",
        "true",
        "t",
        "yes",
        "y",
    }
    app.run(debug=debug)
