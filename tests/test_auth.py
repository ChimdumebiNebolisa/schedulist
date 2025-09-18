import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from app import app, db, google, User
from sqlalchemy import select


def test_authorize_with_email(client, monkeypatch):
    class DummyResp:
        def __init__(self, data):
            self._data = data
            self.ok = True

        def json(self):
            return self._data

    monkeypatch.setattr(google, "authorize_access_token", lambda: {})
    monkeypatch.setattr(
        google,
        "get",
        lambda url, token=None: DummyResp({"sub": "abc123", "email": "user@example.com"}),
    )

    response = client.get("/authorize")
    assert response.status_code == 302
    with app.app_context():
        user = db.session.execute(
            select(User).filter_by(google_id="abc123")
        ).scalar_one_or_none()
        assert user is not None
        assert user.email == "user@example.com"


def test_authorize_without_email(client, monkeypatch):
    class DummyResp:
        def __init__(self, data):
            self._data = data
            self.ok = True

        def json(self):
            return self._data

    monkeypatch.setattr(google, "authorize_access_token", lambda: {})
    monkeypatch.setattr(
        google,
        "get",
        lambda url, token=None: DummyResp({"sub": "abc123"}),
    )

    response = client.get("/authorize")
    assert response.status_code == 400
    assert b"Email claim missing" in response.data


def test_authorize_access_token_error(client, monkeypatch):
    def raise_error():
        raise RuntimeError("boom")

    monkeypatch.setattr(google, "authorize_access_token", raise_error)

    response = client.get("/authorize")
    assert response.status_code == 400
    assert b"Failed to authorize access token" in response.data


def test_userinfo_fetch_error(client, monkeypatch):
    monkeypatch.setattr(google, "authorize_access_token", lambda: {})

    def raise_error(url, token=None):  # pragma: no cover - monkeypatched function
        raise RuntimeError("boom")

    monkeypatch.setattr(google, "get", raise_error)

    response = client.get("/authorize")
    assert response.status_code == 500
    assert b"Failed to parse user information" in response.data
