from datetime import datetime
import os
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

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
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    user_id = session["user_id"]
    tasks_by_quadrant = {
        1: Task.query.filter_by(quadrant=1, user_id=user_id).all(),
        2: Task.query.filter_by(quadrant=2, user_id=user_id).all(),
        3: Task.query.filter_by(quadrant=3, user_id=user_id).all(),
        4: Task.query.filter_by(quadrant=4, user_id=user_id).all(),
    }

    return render_template("index.html", tasks=tasks_by_quadrant, user=session.get("user"))

@app.route("/login")
def login():
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/login/callback")
def authorize():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    session["user"] = user_info

    user = User.query.filter_by(username=user_info["email"]).first()
    if not user:
        user = User(username=user_info["email"])
        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return redirect(url_for("index"))

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

    return render_template('add_task.html', user=session.get("user"))

if __name__ == '__main__':
    app.run()
