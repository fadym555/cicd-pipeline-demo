from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz_returns_ok():
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_version_defaults_to_dev(monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    assert client.get("/version").json() == {"version": "dev"}


def test_version_reads_env(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "1.2.3")
    assert client.get("/version").json() == {"version": "1.2.3"}
