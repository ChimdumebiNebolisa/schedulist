from datetime import date

from models import db, Task, User
from sqlalchemy import select

def test_root_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to Schedulist" in response.data


def test_login_required(client):
    """The dashboard view should redirect anonymous users to login."""
    response = client.get("/dashboard")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_dashboard_template_renders(logged_in_client):
    """The dashboard page should render successfully for logged-in users."""
    response = logged_in_client.get("/dashboard")
    assert response.status_code == 200
    assert b"Dashboard" in response.data
    assert b"No tasks yet." in response.data


def test_tasks_limited_to_session_user(client, app):
    """Accessing another user's task should return 403."""
    user1 = User(username="u1@example.com", google_id="gid1", email="u1@example.com")
    user2 = User(username="u2@example.com", google_id="gid2", email="u2@example.com")
    db.session.add_all([user1, user2])
    db.session.commit()
    task = Task(title="Test", quadrant=1, user_id=user1.id)
    db.session.add(task)
    db.session.commit()

    with client.session_transaction() as sess:
        sess["user_id"] = user2.id

    resp = client.get(f"/tasks/{task.id}/toggle")
    assert resp.status_code == 403


def test_task_crud_operations(logged_in_client, user):
    """Create, update, toggle and delete a task for the logged in user."""
    # Create
    resp = logged_in_client.post(
        "/add",
        data={"title": "New", "quadrant": "1"},
        follow_redirects=False,
    )
    assert resp.status_code == 302
    task = db.session.execute(
        select(Task).filter_by(title="New", user_id=user.id)
    ).scalar_one_or_none()
    assert task is not None

    # Update
    resp = logged_in_client.post(
        f"/task/{task.id}/edit",
        data={
            "title": "Updated",
            "description": "desc",
            "quadrant": "2",
            "deadline": date.today().strftime("%Y-%m-%d"),
        },
    )
    assert resp.status_code == 302
    task = db.session.get(Task, task.id)
    assert task.title == "Updated"
    assert task.quadrant == 2
    assert task.description == "desc"
    assert task.deadline == date.today()

    # Toggle completion
    resp = logged_in_client.get(f"/tasks/{task.id}/toggle")
    assert resp.status_code == 302
    task = db.session.get(Task, task.id)
    assert task.completed is True

    # Delete
    resp = logged_in_client.post(f"/task/{task.id}/delete")
    assert resp.status_code == 302

    assert Task.query.get(task.id) is None

    assert db.session.get(Task, task.id) is None


def test_add_task_invalid_deadline(logged_in_client):
    resp = logged_in_client.post(
        "/add",
        data={"title": "Bad", "quadrant": "1", "deadline": "not-a-date"},
    )
    assert resp.status_code == 400
    assert b"Invalid date format" in resp.data
    assert Task.query.filter_by(title="Bad").first() is None


def test_edit_task_invalid_deadline(logged_in_client, user):
    task = Task(title="T", quadrant=1, user_id=user.id)
    db.session.add(task)
    db.session.commit()
    resp = logged_in_client.post(
        f"/task/{task.id}/edit",
        data={"title": "T", "quadrant": "1", "deadline": "not-a-date"},
    )
    assert resp.status_code == 400
    assert b"Invalid date format" in resp.data
    db.session.refresh(task)
    assert task.deadline is None

