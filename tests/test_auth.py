import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from app import app, google, User

from app import app, db, google, User
from sqlalchemy import select


def test_authorize_with_email(client, monkeypatch):
    monkeypatch.setattr(google, "authorize_access_token", lambda: {})
    monkeypatch.setattr(
        google,
        "parse_id_token",
        lambda token: {"sub": "abc123", "email": "user@example.com"},
    )

    response = client.get("/login/callback")
    assert response.status_code == 302
    with app.app_context():
        user = db.session.execute(
            select(User).filter_by(google_id="abc123")
        ).scalar_one_or_none()
        assert user is not None
        assert user.email == "user@example.com"


def test_authorize_without_email(client, monkeypatch):
    monkeypatch.setattr(google, "authorize_access_token", lambda: {})
    monkeypatch.setattr(google, "parse_id_token", lambda token: {"sub": "abc123"})

    response = client.get("/login/callback")
    assert response.status_code == 400
    assert b"Email claim missing" in response.data
