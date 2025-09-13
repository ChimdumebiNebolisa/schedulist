import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, db, google, User


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
        user = User.query.filter_by(google_id="abc123").first()
        assert user is not None
        assert user.email == "user@example.com"


def test_authorize_without_email(client, monkeypatch):
    monkeypatch.setattr(google, "authorize_access_token", lambda: {})
    monkeypatch.setattr(google, "parse_id_token", lambda token: {"sub": "abc123"})

    response = client.get("/login/callback")
    assert response.status_code == 400
    assert b"Email claim missing" in response.data
