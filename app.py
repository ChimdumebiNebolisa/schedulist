from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from models import db, User, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedulist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    # Create a default user for now until authentication is implemented
    if not User.query.first():
        demo = User(username="demo")
        db.session.add(demo)
        db.session.commit()


@app.route('/')
def index():
    tasks_by_quadrant = {
        1: Task.query.filter_by(quadrant=1).all(),
        2: Task.query.filter_by(quadrant=2).all(),
        3: Task.query.filter_by(quadrant=3).all(),
        4: Task.query.filter_by(quadrant=4).all(),
    }
    return render_template("index.html", tasks=tasks_by_quadrant)


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description')
        deadline_str = request.form.get('deadline')
        quadrant = int(request.form['quadrant'])
        user = User.query.first()

        task = Task(title=title, description=description, quadrant=quadrant, user_id=user.id)
        if deadline_str:
            task.deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()

        db.session.add(task)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_task.html')


if __name__ == '__main__':
    app.run()
