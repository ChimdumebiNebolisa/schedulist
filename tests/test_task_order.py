import os
import sys
from datetime import date

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, db, Task, User


@pytest.fixture(autouse=True)
def clean_db():
    """Ensure a clean database before each test."""
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_tasks_ordered_and_deadline_displayed(client):
    with app.app_context():
        user = User(username="user", google_id="gid", email="user@example.com")
        db.session.add(user)
        db.session.commit()
        t_late = Task(
            title="late", quadrant=1, user_id=user.id, deadline=date(2024, 1, 1)
        )
        t_early = Task(
            title="early", quadrant=1, user_id=user.id, deadline=date(2023, 1, 1)
        )
        db.session.add_all([t_late, t_early])
        db.session.commit()
        user_id = user.id

    with client.session_transaction() as sess:
        sess["user_id"] = user_id
        sess["user"] = {"email": "user@example.com"}

    response = client.get("/dashboard")
    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert "2023-01-01" in text
    assert "2024-01-01" in text
    assert text.index("early") < text.index("late")
