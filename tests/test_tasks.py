from datetime import date

from models import db, Task, User


def test_login_required(client):
    """The index view should redirect anonymous users to login."""
    response = client.get("/")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


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
    task = Task.query.filter_by(title="New", user_id=user.id).first()
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
    task = Task.query.get(task.id)
    assert task.title == "Updated"
    assert task.quadrant == 2
    assert task.description == "desc"
    assert task.deadline == date.today()

    # Toggle completion
    resp = logged_in_client.get(f"/tasks/{task.id}/toggle")
    assert resp.status_code == 302
    task = Task.query.get(task.id)
    assert task.completed is True

    # Delete
    resp = logged_in_client.post(f"/task/{task.id}/delete")
    assert resp.status_code == 302
    assert Task.query.get(task.id) is None
