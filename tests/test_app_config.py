import importlib.util
from pathlib import Path

import pytest


def test_app_requires_secret_key(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.setenv("GOOGLE_CLIENT_ID", "test-client-id")
    monkeypatch.setenv("GOOGLE_CLIENT_SECRET", "test-client-secret")

    module_path = Path(__file__).resolve().parents[1] / "app.py"
    spec = importlib.util.spec_from_file_location("app_missing_secret", module_path)
    module = importlib.util.module_from_spec(spec)

    with pytest.raises(RuntimeError, match="SECRET_KEY environment variable not set"):
        spec.loader.exec_module(module)
